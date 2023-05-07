from pydantic import BaseModel


class Token(BaseModel):
    data: str
    email: str
    validated: bool


class Table(BaseModel):
    id: str
    reserved: bool

    class Config:
        orm_mode = True


class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    wxid: str

    class Config:
        orm_mode = True
