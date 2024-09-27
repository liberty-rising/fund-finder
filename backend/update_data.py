from sqlalchemy.orm import Session
from database import SessionLocal
from api_client import EUFundingAPIClient
from crud import create_or_update_grant_tender
from schemas import EUFTCreate
from dateutil import parser
from datetime import datetime, timezone


def update_grants_tenders():
    db = SessionLocal()
    api_client = EUFundingAPIClient()

    try:
        data = api_client.get_grants_and_tenders()
        for item in data.get("results", []):
            try:
                metadata = item.get("metadata", {})
                grant_tender = EUFTCreate(
                    identifier=metadata.get("identifier", [""])[0],
                    title=item.get("title") or metadata.get("title", [""])[0],
                    description=item.get("summary") or "",
                    status=metadata.get("status", [""])[0],
                    call_identifier=metadata.get("callIdentifier", [""])[0],
                    topic_identifier=metadata.get("identifier", [""])[0],
                    publication_date=parse_date(metadata.get("startDate", [""])[0]),
                    deadline_date=parse_date(
                        metadata.get("deadlineDate", [""])[0]
                        if metadata.get("deadlineDate")
                        else None
                    ),
                )
                create_or_update_grant_tender(db, grant_tender)
            except Exception as e:
                print(f"Error processing item: {e}")
                print(f"Problematic item: {item}")
    except Exception as e:
        print(f"Error fetching or processing data: {e}")
    finally:
        db.close()


def parse_date(date_string):
    if not date_string:
        return None
    try:
        # Parse the date string and convert to UTC
        dt = parser.parse(date_string)
        return dt.astimezone(timezone.utc)
    except ValueError:
        print(f"Invalid date format: {date_string}")
        return None


if __name__ == "__main__":
    update_grants_tenders()
