# backend/app/twilio_handler.py
from fastapi import Request
from sqlalchemy.orm import Session
from . import crud
import html

def twilio_response_text(text: str):
    # Return TwiML XML
    # Ensure to escape special chars
    escaped = html.escape(text)
    return f'<?xml version="1.0" encoding="UTF-8"?><Response><Message>{escaped}</Message></Response>'

def handle_incoming_sms(db: Session, from_number: str, body_text: str):
    """
    body_text: raw message body from WhatsApp (Twilio)
    from_number: e.g., 'whatsapp:+1415XXXXXXX' or '+1415XXX' depending on Twilio config
    """
    # Normalize contact number (keep Twilio's prefix if present)
    contact = from_number.strip()

    text = body_text.strip()
    # Basic normalization
    text_lower = text.lower()

    state = crud.get_or_create_state(db, contact)
    # flow: ask_product -> ask_name -> ask_review -> finalize
    if state.step == "ask_product":
        # If user provided product in a single shot message, accept it
        if text_lower not in ("hi", "hello", "hey", "start"):
            # treat message as product name
            crud.update_state(db, contact, step="ask_name", temp_product_name=text)
            reply = f"What's your name?"
            return twilio_response_text(reply)
        else:
            return twilio_response_text("Which product is this review for?")

    elif state.step == "ask_name":
        # text is user name
        crud.update_state(db, contact, step="ask_review", temp_user_name=text)
        reply = f"Please send your review for {state.temp_product_name or 'the product'}."
        return twilio_response_text(reply)

    elif state.step == "ask_review":
        # text is the review -> create review record
        product = state.temp_product_name or "Unknown Product"
        user = state.temp_user_name or "Unknown User"
        review_text = text
        crud.create_review(db, contact_number=contact, user_name=user, product_name=product, product_review=review_text)
        crud.clear_state(db, contact)
        return twilio_response_text(f"Thanks {user} -- your review for {product} has been recorded.")
    else:
        crud.update_state(db, contact, step="ask_product")
        return twilio_response_text("Which product is this review for?")
