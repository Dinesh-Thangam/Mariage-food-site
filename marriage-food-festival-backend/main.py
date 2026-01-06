from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

from fastapi.middleware.cors import CORSMiddleware



# Load environment variables


load_dotenv()

allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
allowed_methods = os.getenv("ALLOWED_METHODS", "*").split(",")
allowed_headers = os.getenv("ALLOWED_HEADERS", "*").split(",")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=allowed_methods,
    allow_headers=allowed_headers,
)

MONGO_URI = os.getenv("MONGO_URI")  # Reads your MongoDB URI from .env

# Connect to MongoDB
client = AsyncIOMotorClient(MONGO_URI)
db = client.marriage_food_festival  # Database (auto-created if missing)


# Pydantic model for input
class Item(BaseModel):
    name: str
    email: str
    description: str

# Helper function to convert MongoDB document to JSON-serializable dict
def item_helper(item) -> dict:
    return {
        "item_id": str(item["_id"]),
        "name": item["name"],
        "email": item["email"],
        "description": item["description"],
    }

@app.get("/")
async def root():
    return {"message": "Marriage Food Festival Backend Running"}

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    result = await db.items.insert_one(item_dict)  # Save to MongoDB
    saved_item = await db.items.find_one({"_id": result.inserted_id})
    return item_helper(saved_item)

@app.get("/items/")
async def get_items():
    items_cursor = db.items.find()  # Fetch all items from 'items' collection
    items = []
    async for item in items_cursor:
        items.append(item_helper(item))
    return items

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",          # points to your FastAPI app
        host="127.0.0.1",    # localhost
        port=int(os.getenv("PORT", 5000)),  # uses PORT from .env or defaults to 5000
        reload=True          # auto-reload on code changes
    )