from datetime import datetime

from pydantic import BaseModel


class library(BaseModel):
    id: int
    title: str
    author: str
    year: int
    status: str

class CreateBook(BaseModel):
    title: str
    author: str
    year: int

class IdBook(BaseModel):
    id: int

class UpdateBook(BaseModel):
    title: str
    author: str
    year: int
    status: str

