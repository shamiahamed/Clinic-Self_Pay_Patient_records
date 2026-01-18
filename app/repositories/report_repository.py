import logging
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.logger.api_logger import log_execution
from app.core.exception import DatabaseException

logger = logging.getLogger(__name__)

SORT_MAP = {
    "firstname": "firstname",
    "lastname": "lastname",
    "dob": "dob",
    "last_dos": "last_dos",
    "balance": "patient_balance",
    "billed": "billed_total",
    "paid": "patient_payments_total"
}

@log_execution
async def fetch_self_pay_patients(
    db: AsyncSession,
    clinic_id: int,
    filters: dict,
    page: int,
    page_size: int,
    sort_by: str,
    sort_dir: str
):
    sort_column = SORT_MAP.get(sort_by, "lastname")
    sort_dir = "DESC" if sort_dir.lower() == "desc" else "ASC"
    offset = (page - 1) * page_size
    
    query_params = {"clinic_id": clinic_id, "limit": page_size, "offset": offset}

    try:
        where_clauses = ["p.CLINIC_ID = :clinic_id", "p.MARK_AS_DELETE = 0"]
        if filters.get("search"):
            where_clauses.append("(p.FIRST_NAME LIKE :search OR p.LAST_NAME LIKE :search)")
            query_params["search"] = f"%{filters['search']}%"

        billed_sq = """(SELECT COALESCE(SUM(BILLED), 0) FROM CLAIM 
                        WHERE PATIENT_ID = p.PATIENT_ID AND CLINIC_ID = :clinic_id
                        AND (PRIMARY_PAYER_ID = 0 OR PRIMARY_PAYER_NAME = 'SELF PAY'))"""
        
        paid_sq = """(
                  SELECT COALESCE(SUM(py.AMOUNT), 0)
                  FROM PAYMENT py
                  JOIN CLAIM cl ON cl.VISIT_ID = py.VISIT_ID
                  WHERE cl.PATIENT_ID = p.PATIENT_ID
                  AND py.CLINIC_ID = :clinic_id
                  AND py.PAYER_TYPE = 3
                  AND py.MARK_AS_DELETE = 0
                  AND cl.MARK_AS_DELETE = 0
                )"""

        inner_query = f"""
            SELECT 
              p.PATIENT_ID AS patient_id,
              p.FIRST_NAME AS firstname,
              p.LAST_NAME AS lastname,
              DATE(p.DOB) AS dob,
              p.LAST_DOS AS last_dos,
              REPLACE(p.PROVIDER_NAME, ',', ', ') AS last_provider,
              p.FACILITY_NAME AS last_facility,
              {billed_sq} AS billed_total,
              {paid_sq} AS patient_payments_total,
              ({billed_sq} - {paid_sq}) AS patient_balance
            FROM PATIENT p
            WHERE {" AND ".join(where_clauses)}
        """

        final_base = f"SELECT * FROM ({inner_query}) AS sub"
        if filters.get("min_balance"):
            final_base += " WHERE patient_balance >= :min_balance"
            query_params["min_balance"] = filters["min_balance"]

        count_sql = f"SELECT COUNT(*) FROM ({final_base}) AS count_ref"
        res_count = await db.execute(text(count_sql), query_params)
        total = res_count.scalar() or 0

        data_sql = f"{final_base} ORDER BY {sort_column} {sort_dir} LIMIT :limit OFFSET :offset"
        res_data = await db.execute(text(data_sql), query_params)
        rows = res_data.mappings().all()

        return rows, total

    except Exception as e:
        await db.rollback()
        logger.error(f"Fetch Patients failed: {str(e)}", exc_info=True)
        # Raising this triggers the handler in main.py automatically
        raise DatabaseException(str(e))