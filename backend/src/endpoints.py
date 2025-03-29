from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from services.calculate_usd import calculate_usd
from schemas.expense import ExpenseSchema
from models.expense import Expense
from database import get_db

router = APIRouter()

@router.get("/expenses")
def get_expenses(start_date: str = Query(None), end_date: str = Query(None), db: Session = Depends(get_db)):
    if start_date and end_date:
        start_dt = datetime.strptime(start_date, '%d.%m.%Y')
        end_dt = datetime.strptime(end_date, '%d.%m.%Y') + timedelta(days=1) - timedelta(seconds=1)

        return db.query(Expense).filter(
            Expense.date >= start_dt,
            Expense.date <= end_dt
        ).all()
    
    return db.query(Expense).all()

@router.post("/expenses", status_code=201)
def create_expense(expense: ExpenseSchema, db: Session = Depends(get_db)):
    new_expense = Expense(
        user_id=expense.user_id, 
        name=expense.name, 
        amount_uah=expense.amount_uah,
        date=Expense.parse_date(expense.date),
        amount_usd=calculate_usd(expense.amount_uah),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

@router.get("/expenses/{id}")
def get_expense_by_id(id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="expense not found")
    return expense

@router.put("/expenses/{id}")
def update_expense(id: int, expense: ExpenseSchema, db: Session = Depends(get_db)):
    edited_expense = db.query(Expense).filter(Expense.id == id).first()
    
    if not edited_expense:
        raise HTTPException(status_code=404, detail="expense not found")
    
    edited_expense.name = expense.name
    edited_expense.amount_uah = expense.amount_uah
    edited_expense.amount_usd = calculate_usd(expense.amount_uah)
    edited_expense.updated_at = datetime.now()
    
    db.commit()
    db.refresh(edited_expense)
    return edited_expense

@router.delete("/expenses/{id}")
def delete_expense(id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="expense not found")
    name = expense.name
    db.delete(expense)
    db.commit()
    return {"message": f"expense {name} has been deleted successfully"}

def get_router() -> APIRouter:
    return router
