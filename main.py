from fastapi import FastAPI, HTTPException, Request, status
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="FastAPI Connection Test App",
    description="Test API connections with various methods.",
)

# Sample data (in-memory database simulation)
items = {
    1: {"name": "Item 1", "description": "Description 1"},
    2: {"name": "Item 2", "description": "Description 2"},
}


class Item(BaseModel):
    name: str
    description: Optional[str] = None


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the FastAPI Connection Test App!"}


@app.get("/items/", response_model=List[Item], tags=["Items"])
async def read_items():
    return list(items.values())


@app.get("/items/{item_id}", response_model=Item, tags=["Items"])
async def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]


@app.post("/items/", response_model=Item, status_code=201, tags=["Items"])
async def create_item(item: Item):
    next_item_id = len(items) + 1
    items[next_item_id] = item.dict()
    return items[next_item_id]


@app.put("/items/{item_id}", response_model=Item, tags=["Items"])
async def update_item(item_id: int, item: Item):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id] = item.dict()
    return items[item_id]


@app.patch("/items/{item_id}", response_model=Item, tags=["Items"])
async def partial_update_item(item_id: int, item: Item):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    existing_item = items[item_id]
    updated_item = item.dict(exclude_unset=True)  # Only update provided fields
    existing_item.update(updated_item)
    items[item_id] = existing_item
    return existing_item


@app.delete("/items/{item_id}", status_code=204, tags=["Items"])
async def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
    return {}  # Return empty body for 204


@app.head("/items/{item_id}", status_code=200, tags=["Items"])
async def head_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {}  # Return empty body with headers only


@app.options("/items/{item_id}", status_code=200, tags=["Items"])
async def options_item(request: Request, item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"allowed_methods": ["GET", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]}
