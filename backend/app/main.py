# backend/app/main.py
from fastapi import FastAPI, Request, Response, Depends
from fastapi.responses import JSONResponse, PlainTextResponse
from . import database, models, twilio_handler, crud, schemas
from sqlalchemy.orm import Session
import uvicorn
import os

app = FastAPI(title="WhatsApp Product Review Collector")

# create tables (auto)
models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/twilio/webhook", response_class=PlainTextResponse)
async def twilio_webhook(request: Request, db: Session = Depends(get_db)):
    # Twilio sends form-encoded payload with 'From' and 'Body'
    form = await request.form()
    from_number = form.get("From") or form.get("from") or ""
    body = form.get("Body") or form.get("body") or ""
    xml_response = twilio_handler.handle_incoming_sms(db, from_number, body)
    return Response(content=xml_response, media_type="text/xml")

@app.get("/api/reviews", response_model=list[schemas.ReviewOut])
def get_reviews(db: Session = Depends(get_db)):
    rows = crud.get_all_reviews(db, limit=1000)
    return rows

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)

