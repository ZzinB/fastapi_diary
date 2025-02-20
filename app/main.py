from fastapi import FastAPI, Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import User

app = FastAPI()

@app.get("/")
async def main(db: AsyncSession = Depends(get_db)):
    return {"HIiii"}

