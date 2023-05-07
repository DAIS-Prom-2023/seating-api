import os
import random

from fastapi import FastAPI, Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks
from starlette.middleware.cors import CORSMiddleware

import crud
import models
import schemas
import mail
from database import get_db, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://daisprom23.com",
    "http://192.168.1.134:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if not os.path.exists('./database.db'):
    session = get_db()
    names = "path3754, path3742, path3778, path3790, path3766, path3802, path3814, path4014, path4026, path3826, path3830, path3850, path3866, path4162, path4242, path4094, path4050, path4066, path4038, path4254, path4126, path3882, path4082, path4106, path3894, path4138, path3906, path4150, path3918, path4186, path4174, path3942, path3930, path4198, path3954, path4222, path3966, path3978, path3990, path4232, path4210, path4002"
    name_list = names.split(', ')
    for name in name_list:
        new_table = models.Table(
            id=name,
        )
        session.add(new_table)
        session.commit()


@app.post("/request-token/{email}")
def request_token(
        email: str,
        bg: BackgroundTasks,
        db: Session = Depends(get_db)
):
    try:
        crud.delete_token_by_email(db, email)  # delete token for this email if it exists
        token_data = ' '.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
        while crud.get_token_by_data(db, token_data) is not None:
            token_data = ' '.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
        crud.create_token(db, email, token_data)
        mail.send_email_background('DAIS Prom 2023: Verification Code', email, {'token_data': token_data},
                                   bg)
    except ValidationError:
        raise HTTPException(
            status_code=404,
            detail="Please check your inputs"
        )
    return {"detail": "Requested token!"}


@app.post("/validate-token/{token_data}")
def validate_token(
        token_data: str,
        db: Session = Depends(get_db)
):
    db_token = crud.get_token_by_data(db, token_data)
    if db_token is None:
        raise HTTPException(
            status_code=404,
            detail="Token does not exist"
        )
    db_token.validated = True
    db.commit()
    db.refresh(db_token)
    return {"detail": "Validated token!"}


@app.post("/reserve-table/{table_id}/")
def reserve_table(
        table_id: str,
        user: schemas.User,
        db: Session = Depends(get_db)
):
    db_token = crud.get_token_by_email(db, user.email)
    if db_token is None or not db_token.validated:
        raise HTTPException(
            status_code=404,
            detail="Email not verified"
        )
    db_user = crud.get_user_by_email(db, user.email)
    if db_user is not None:
        raise HTTPException(
            status_code=404,
            detail="You have already made a reservation with this email"
        )
    db_table = crud.get_table(db, table_id)
    if db_table is None:
        raise HTTPException(
            status_code=404,
            detail="This table does not exist"
        )
    elif db_table.reserved:
        raise HTTPException(
            status_code=404,
            detail="This table has already been reserved"
        )

    new_user = crud.create_user(db, user)
    crud.reserve_table(db, new_user.id, table_id)


@app.get("/get-data/")
def get_data(
        db: Session = Depends(get_db)
) -> list[schemas.Table]:
    return crud.get_tables(db, 999)
