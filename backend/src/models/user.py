from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database import Base

class User(Base):    
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, nullable=False, unique=True)
    username = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    
    expenses = relationship("Expense", back_populates="user", cascade="all, delete")
    