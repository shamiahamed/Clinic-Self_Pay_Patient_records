import math
from app.services.report_service import get_self_pay_report

async def self_pay_controller(db, user, filters):
    # Pass the object directly to the service
    rows, total = await get_self_pay_report(db, user, filters)

    # Calculate total pages safely
    total_pages = math.ceil(total / filters.page_size) if filters.page_size > 0 else 0

    return {
        "data": rows,
        "pagination": {
            "page": filters.page,
            "page_size": filters.page_size,
            "total_rows": total,
            "total_pages": total_pages
        }
    }