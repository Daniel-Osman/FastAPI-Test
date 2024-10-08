from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# Define a data model using Pydantic for request body validation
class Item(BaseModel):
    name: str
    description: str | None = None  # Optional field
    price: float
    tax: float | None = None  # Optional field


@app.get("/")  # Root path
async def root():
    return {"message": "Welcome to the FastAPI example!"}


@app.get("/items/{item_id}")  # Path parameter
async def read_item(item_id: int, q: str | None = None):  # Query parameter
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")  # PUT request (for updates)
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "item": item}


@app.post("/items/")  # POST request (for creating new items)
async def create_item(item: Item):
    item_dict = item.model_dump()  # Convert Pydantic model to dictionary
    if item.tax:  # Calculate total price including tax
        item_dict.update({"price_with_tax": item.price + item.tax})
    return item_dict
