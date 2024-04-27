from dotenv import load_dotenv
import os
from fastapi import FastAPI, Request
import databases
import sqlalchemy

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


books = sqlalchemy.Table(
    "books",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(length=255)),
    sqlalchemy.Column("author_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("authors.id")),
)

authors = sqlalchemy.Table(
    "authors",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(length=60))
)


engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all()

app = FastAPI(openapi_prefix="/v1")

@app.on_event("startup")
async def startup():
    await database.connect()
    
    
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/books/")
async def get_all_books():
    """Fetch all books
    TODO: Add pagination
    """
    query = books.select()
    return await database.fetch_all(query=query)

@app.post("/book/")
async def create_book(request: Request):
    data = await request.json()
    query = books.insert().values(**data)
    last_record_id = await database.execute(query=query)
    return {"id": last_record_id}
    
@app.put("/book/")
async def update_book(request: Request):
    data = await request.json()
    _id = data.pop("id")
    query = books.update().where(books.c.id == _id).values(**data)
    last_record_id = await database.execute(query=query)
    return {"id": last_record_id}



@app.get("/books/{book_id}")
async def get_book(book_id: int):
    pass



