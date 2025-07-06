import json
import uuid
import random
import logging
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, validator
import pandas as pd
from faker import Faker
import os

# Setup logging
logging.basicConfig(
    filename="survey_validation.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

fake = Faker()

# -----------------------------
# 1. Define Pydantic Schema
# -----------------------------
class DisneySurvey(BaseModel):
    guest_id: str
    visit_date: datetime
    park_location: str
    rating: int = Field(..., ge=1, le=10)
    comment: Optional[str]
    language: str
    ticket_type: str
    wait_time: Optional[int] = Field(None, ge=0)
    spend_usd: Optional[float] = Field(None, ge=0)
    email_consent: bool
    wifi_rating: Optional[int] = Field(None, ge=1, le=10)
    staff_friendliness: Optional[int] = Field(None, ge=1, le=10)
    cleanliness: Optional[int] = Field(None, ge=1, le=10)
    favorite_ride: Optional[str]
    transaction_uuid: UUID

    @validator('language')
    def validate_language(cls, v):
        allowed = ['en', 'fr', 'es', 'jp']
        if v not in allowed:
            raise ValueError(f"Unsupported language: {v}")
        return v

# -----------------------------
# 2. Generate Sample Data
# -----------------------------
def generate_sample_data(n=100):
    rides = ["Space Mountain", "Big Thunder", "Haunted Mansion", "Pirates", "Test Track", "Soarin"]
    parks = ["Magic Kingdom", "EPCOT", "Disneyland Paris", "Tokyo DisneySea"]
    langs = ['en', 'fr', 'es', 'jp']
    ticket_types = ['standard', 'hopper', 'vip']

    data = []
    for _ in range(n):
        guest_id = fake.uuid4()[:8]
        visit_date = fake.date_between(start_date='-1y', end_date='today').isoformat()
        park_location = random.choice(parks)
        rating = random.randint(1, 10)
        comment = fake.sentence(nb_words=6)
        language = random.choice(langs)
        ticket_type = random.choice(ticket_types)
        wait_time = random.randint(5, 90)
        spend_usd = round(random.uniform(50, 300), 2)
        email_consent = random.choice([True, False])
        wifi_rating = random.randint(1, 10)
        staff_friendliness = random.randint(1, 10)
        cleanliness = random.randint(1, 10)
        favorite_ride = random.choice(rides)
        txn_uuid = str(uuid.uuid4())

        record = {
            "guest_id": guest_id,
            "visit_date": visit_date,
            "park_location": park_location,
            "rating": rating,
            "comment": comment,
            "language": language,
            "ticket_type": ticket_type,
            "wait_time": wait_time,
            "spend_usd": spend_usd,
            "email_consent": email_consent,
            "wifi_rating": wifi_rating,
            "staff_friendliness": staff_friendliness,
            "cleanliness": cleanliness,
            "favorite_ride": favorite_ride,
            "transaction_uuid": txn_uuid
        }

        data.append(record)

    return data

# -----------------------------
# 3. Validate Records
# -----------------------------
def validate_records(records):
    valid = []
    invalid = []
    for i, record in enumerate(records):
        try:
            validated = DisneySurvey(**record)
            valid.append(validated.dict())
            logging.info(f"✅ Record {i} passed validation")
        except Exception as e:
            invalid.append({"record": record, "error": str(e)})
            logging.error(f"❌ Record {i} failed: {e}")
    return valid, invalid

# -----------------------------
# 4. Run Full Flow
# -----------------------------
if __name__ == "__main__":
    logging.info("🚀 Starting survey data validation pipeline")

    # Generate data
    survey_data = generate_sample_data(100)
    with open("sample_disney_surveys.json", "w") as f:
        json.dump(survey_data, f, indent=2)

    logging.info(f"✅ Generated {len(survey_data)} sample records")

    # Validate
    valid_records, invalid_records = validate_records(survey_data)
    logging.info(f"✅ {len(valid_records)} records valid")
    logging.info(f"⚠️ {len(invalid_records)} records invalid")

    # Save valid data
    df_valid = pd.DataFrame(valid_records)
    df_valid.to_parquet("validated_surveys.parquet", index=False)
    df_valid.to_csv("validated_surveys.csv", index=False)

    logging.info("📁 Valid records saved as Parquet and CSV")

    # Save failed records
    if invalid_records:
        with open("invalid_surveys.json", "w") as f:
            json.dump(invalid_records, f, indent=2)
        logging.warning("⚠️ Some records failed and were saved in invalid_surveys.json")

    logging.info("✅ Survey data pipeline completed")
