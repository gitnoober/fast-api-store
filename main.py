from dotenv import load_dotenv
import os
from fastapi import FastAPI, Request
import databases
import sqlalchemy

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL)

# Bind the engine to the metadata
metadata.bind = engine


books = sqlalchemy.Table(
    "books",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(length=255)),
    sqlalchemy.Column(
        "author_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("authors.id")
    ),
)

authors = sqlalchemy.Table(
    "authors",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(length=60)),
)

metadata.create_all()

app = FastAPI()


@app.on_event("startup")
async def startup():
    """
    Startup event handler for the FastAPI app.

    This function is called when the app is starting up. It connects to the database using the `database.connect()` method.

    Parameters:
        None

    Returns:
        None
    """
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    """
    Shutdown event handler for the FastAPI app.

    This function is called when the app is shutting down. It disconnects the database connection.

    Parameters:
        None

    Returns:
        None
    """
    await database.disconnect()


@app.get("/books/")
async def get_all_books():
    """Fetch all books
    TODO: Add pagination
    """
    query = books.select()
    return await database.fetch_all(query=query)


@app.post("/author/")
async def create_author(request: Request):
    """
    Creates a new author in the database.

    Parameters:
        - request (Request): The HTTP request object containing the author data.

    Returns:
        - dict: A dictionary containing the ID of the newly created author.
    """
    data = await request.json()
    query = authors.insert().values(**data)
    last_record_id = await database.execute(query=query)
    return {"id": last_record_id}


@app.get("/authors/")
async def get_all_authors():
    """Fetch all books
    TODO: Add pagination
    """
    query = authors.select()
    return await database.fetch_all(query=query)


@app.get("/author/{author_id}")
async def get_author(author_id: int):
    pass


@app.post("/book/")
async def create_book(request: Request):
    """
    Create a new book in the database.

    This function handles the HTTP POST request to the "/book/" endpoint. It expects a JSON payload in the request body containing the data for the new book. The function inserts the book data into the "books" table using the SQLAlchemy ORM and returns the ID of the newly created record.

    Parameters:
        - request (Request): The HTTP request object containing the book data.

    Returns:
        - dict: A dictionary containing the ID of the newly created book.
    """
    data = await request.json()
    query = books.insert().values(**data)
    last_record_id = await database.execute(query=query)
    return {"id": last_record_id}


@app.put("/book/")
async def update_book(request: Request):
    """
    Update a book in the database.

    This function handles the HTTP PUT request to the "/book/" endpoint. It expects a JSON payload in the request body containing the updated data for the book. The function updates the book data in the "books" table using the SQLAlchemy ORM and returns the ID of the updated record.

    Parameters:
        - request (Request): The HTTP request object containing the updated book data.

    Returns:
        - dict: A dictionary containing the ID of the updated book.
    """
    data = await request.json()
    _id = data.pop("id")
    query = books.update().where(books.c.id == _id).values(**data)
    last_record_id = await database.execute(query=query)
    return {"id": last_record_id}


@app.get("/books/{book_id}")
async def get_book(book_id: int):
    pass
