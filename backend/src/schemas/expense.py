from typing import Optional

from pydantic import BaseModel, Field

class ExpenseSchema(BaseModel):
    user_id: Optional[int] = None
    name: str = Field(..., example='Name')
    amount_uah: float = Field(..., example=100.00)
    date: Optional[str] = None
    