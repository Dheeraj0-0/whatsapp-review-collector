# backend/app/crud.py
from . import models, database
from sqlalchemy.orm import Session
from datetime import datetime

def get_or_create_state(db: Session, contact: str):
    state = db.query(models.ConversationState).filter_by(contact_number=contact).first()
    if not state:
        state = models.ConversationState(contact_number=contact, step="ask_product")
        db.add(state)
        db.commit()
        db.refresh(state)
    return state

def update_state(db: Session, contact: str, **kwargs):
    state = db.query(models.ConversationState).filter_by(contact_number=contact).first()
    if not state:
        state = models.ConversationState(contact_number=contact, **kwargs)
        db.add(state)
    else:
        for k,v in kwargs.items():
            setattr(state, k, v)
    db.commit()
    db.refresh(state)
    return state

def clear_state(db: Session, contact: str):
    state = db.query(models.ConversationState).filter_by(contact_number=contact).first()
    if state:
        db.delete(state)
        db.commit()

def create_review(db: Session, contact_number: str, user_name: str, product_name: str, product_review: str):
    review = models.Review(
        contact_number=contact_number,
        user_name=user_name,
        product_name=product_name,
        product_review=product_review
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

def get_all_reviews(db: Session, limit: int = 100):
    return db.query(models.Review).order_by(models.Review.created_at.desc()).limit(limit).all()
