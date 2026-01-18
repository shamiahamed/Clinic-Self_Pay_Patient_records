from app.repositories.report_repository import fetch_self_pay_patients
from app.core.exception import DatabaseException

async def get_self_pay_report(db, user, filters):
    """
    Receives the 'filters' Pydantic object and extracts what the repo needs.
    """
    try:
        # 1. Map fields for the repository WHERE clause
        repo_filters = {
            "search": filters.search,
            "dob_from": filters.dob_from,
            "dob_to": filters.dob_to,
            "last_dos_from": filters.last_dos_from,
            "last_dos_to": filters.last_dos_to,
            "min_balance": filters.min_balance
        }

        # 2. Call the repository using object attributes
        return await fetch_self_pay_patients(
            db=db,
            clinic_id=filters.clinic_id,
            filters=repo_filters,
            page=filters.page,
            page_size=filters.page_size,
            sort_by=filters.sort_by,
            sort_dir=filters.sort_dir
        )
        
    except Exception as e:
        # Using the custom exception you created
        raise DatabaseException(f"Report Service Error: {str(e)}")