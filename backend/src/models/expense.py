from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship

from database import Base

class Expense(Base):    
    __tablename__ = 'expenses'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.telegram_id', ondelete='CASCADE'), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    amount_uah = Column(DECIMAL(10, 2), nullable=False)
    amount_usd = Column(DECIMAL(10, 2), nullable=False)
    date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    
    user = relationship("User", back_populates="expenses")
    
    @staticmethod
    def parse_date(date_str: str) -> datetime:
        return datetime.strptime(date_str, '%d.%m.%Y')