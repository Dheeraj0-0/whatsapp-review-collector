# backend/app/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy import Enum
from .database import Base
from sqlalchemy.sql import expression

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    contact_number = Column(String(50), index=True)
    user_name = Column(String(200))
    product_name = Column(String(200))
    product_review = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ConversationState(Base):
    """
    Temporary in-DB state for multi-step conversation with a contact.
    Keeps flow robust across restarts (unlike in-memory dict).
    """
    __tablename__ = "conversation_states"
    id = Column(Integer, primary_key=True, index=True)
    contact_number = Column(String(50), unique=True, index=True)
    step = Column(String(50), default="ask_product")  # ask_product, ask_name, ask_review, done
    temp_product_name = Column(String(200), nullable=True)
    temp_user_name = Column(String(200), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
