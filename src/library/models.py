from sqlalchemy import Table, Column, Integer, String, TIMESTAMP

from database import metadata

library = Table(
    "library",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("author", String, nullable=True),
    Column("year", Integer, nullable=True),
    Column("status", String, nullable=True),
)
