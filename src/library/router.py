from database import get_async_session
from fastapi import APIRouter, Depends, HTTPException
from library.models import library as library_model
from library.schemas import CreateBook, UpdateBook
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

router = APIRouter(
    prefix="/library",
    tags=["Library"]
)


@router.post("/create/")
async def create_book(new_book: CreateBook, session: AsyncSession = Depends(get_async_session)):
    try:
        query = (
            insert(library_model).
            values(**new_book.model_dump(), status="в наличии")
        )
        await session.execute(query)
        await session.commit()
        return {"status": "success"}
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router.delete("/delete/{id}/")
async def delete_book(book_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(library_model).where(library_model.c.id == book_id)
        result = await session.execute(query)
        await session.commit()
        if result.first() is None:
            return {"status": "book doesn't exist"}
        query = (
            delete(library_model).
            where(library_model.c.id == book_id)
        )
        await session.execute(query)
        await session.commit()
        return {"status": "success"}
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })

@router.get("/get/{id}/")
async def get_book_by_id(book_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(library_model).where(library_model.c.id == book_id)
        result = await session.execute(query)
        await session.commit()
        return {
            "status": "success",
            "data": result.mappings().all(),
            "details": None
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })

@router.get("/filter/{id}/")
async def get_book_filter(
        title: Optional[str] = None,
        author: Optional[str] = None,
        year: Optional[int] = None,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(library_model)

        if title:
            query = query.where(library_model.c.title.contains(title))
        if author:
            query = query.where(library_model.c.author.contains(author))
        if year:
            query = query.where(library_model.c.year == year)

        result = await session.execute(query)
        await session.commit()
        return {
            "status": "success",
            "data": result.mappings().all(),
            "details": None
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })

@router.get("/all/")
async def get_all_books(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(library_model)
        result = await session.execute(query)
        await session.commit()
        return {
            "status": "success",
            "data": result.mappings().all(),
            "details": None
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })

@router.patch("/update/")
async def update_book(book_id: int, book_data: UpdateBook, session: AsyncSession = Depends(get_async_session)):
    try:
        query = (
            update(library_model).
            where(library_model.c.id == book_id).
            values(**book_data.model_dump())
        )
        await session.execute(query)
        await session.commit()
        return {
            "status": "success",
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


