import math
from app.services.report_service import get_self_pay_report
from app.core.messages import AppMessages # Requirement #13

async def self_pay_controller(db, user, filters):
    # 1. Get rows and total count from service
    rows, total = await get_self_pay_report(db, user, filters)

    # 2. Requirement #14: Calculate total pages safely
    total_pages = math.ceil(total / filters.page_size) if filters.page_size > 0 else 0

    # 3. Standardized JSON Output
    return {
        "status": True,
        "message": AppMessages.SUCCESS_FETCH,
        "data": rows,
        "pagination": {
            "page": filters.page,
            "page_size": filters.page_size,
            "total_rows": total,
            "total_pages": total_pages
        }
    }