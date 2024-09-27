from sqlalchemy.orm import Session
from database import SessionLocal
from api_client import EUFundingAPIClient
from crud import create_or_update_grant_tender
from schemas import EUFTCreate
from dateutil import parser
from datetime import datetime, timezone
import math
import logging


def parse_fund_type(fund_type_code):
    fund_type_mapping = {
        "0": "Tender",
        "1": "Grant",
        "2": "Calls for proposals",
        "6": "Funding updates",
        "8": "Cascade funding calls",
    }
    return fund_type_mapping.get(fund_type_code, "Unknown")


def parse_status(status_code):
    status_mapping = {
        "31094501": "Forthcoming",
        "31094502": "Open for submission",
        "31094503": "Closed",
    }
    return status_mapping.get(status_code, "Unknown")


def update_grants_tenders(max_items=None):
    db = SessionLocal()
    api_client = EUFundingAPIClient()
    page_number = 1
    page_size = 100
    total_processed = 0

    try:
        while True:
            data = api_client.get_grants_and_tenders(
                page_number=page_number, page_size=page_size
            )
            results = data.get("results", [])
            total_results = data.get("totalResults", 0)

            for item in results:
                try:
                    metadata = item.get("metadata", {})
                    grant_tender = EUFTCreate(
                        identifier=metadata.get("identifier", [""])[0],
                        title=item.get("title") or metadata.get("title", [""])[0],
                        description=item.get("descriptionByte") or "",
                        keywords=", ".join(metadata.get("keywords", [])),
                        fund_type=parse_fund_type(metadata.get("fundType", [""])[0]),
                        links=", ".join(item.get("links", [])),
                        status=parse_status(metadata.get("status", [""])[0]),
                        call_identifier=metadata.get("callIdentifier", [""])[0],
                        topic_identifier=metadata.get("identifier", [""])[0],
                        topic_conditions=metadata.get("topicConditions", [""])[0],
                        budget=metadata.get("budget", [""])[0],
                        start_date=parse_date(metadata.get("startDate", [""])[0]),
                        deadline_date=parse_date(
                            metadata.get("deadlineDate", [""])[0]
                            if metadata.get("deadlineDate")
                            else None
                        ),
                    )
                    create_or_update_grant_tender(db, grant_tender)
                    total_processed += 1

                    if max_items and total_processed >= max_items:
                        return total_processed

                except Exception as e:
                    print(f"Error processing item: {e}")
                    print(f"Problematic item: {item}")

            if page * page_size >= total_results:
                break

            page += 1

    except Exception as e:
        print(f"Error fetching or processing data: {e}")
    finally:
        db.close()

    return total_processed


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
    total_updated = update_grants_tenders()
    print(f"Total items updated: {total_updated}")
