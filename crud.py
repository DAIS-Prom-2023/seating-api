from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

import models
import schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.User) -> Optional[models.User]:
    new_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        wxid=user.wxid
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_table(db: Session, table_id: str) -> Optional[models.Table]:
    return db.query(models.Table).filter(models.Table.id == table_id).first()


def get_tables(db: Session, limit: int = 100):
    return db.query(models.Table).limit(limit).all()


def reserve_table(db: Session, user_id: int, table_id: str):
    table = get_table(db, table_id)
    table.reserver_id = user_id
    table.reserved = True
    db.commit()
    db.refresh(table)
    return table


def get_token_by_email(db: Session, email: str) -> Optional[models.Token]:
    return db.query(models.Token).filter(models.Token.email == email).first()


def delete_token_by_email(db: Session, email: str):
    db_token = get_token_by_email(db, email)
    if db_token is not None:
        db.delete(db_token)
        db.commit()
    return


def get_token_by_data(db: Session, token_data: str) -> Optional[models.Token]:
    return db.query(models.Token).filter(models.Token.data == token_data).first()


def create_token(db: Session, email: str, token_data: str):
    new_token = models.Token(
        data=token_data,
        email=email
    )
    db.add(new_token)
    db.commit()
    db.refresh(new_token)
    return new_token
