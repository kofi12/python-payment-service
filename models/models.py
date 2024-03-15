from typing import Optional
from sqlmodel import Field, SQLModel, create_engine
from dotenv import load_dotenv
import os


class Seller(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    seller_id: str