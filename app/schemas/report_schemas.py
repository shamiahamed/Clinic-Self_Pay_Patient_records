from pydantic import BaseModel, ConfigDict
from datetime import date
from decimal import Decimal
from typing import List, Optional

# --- REQUEST SCHEMA (The Filters) ---
class SelfPayFilter(BaseModel):
    clinic_id: int
    page: int = 1
    page_size: int = 25
    sort_by: str = "lastname"
    sort_dir: str = "asc"
    search: Optional[str] = None
    dob_from: Optional[date] = None
    dob_to: Optional[date] = None
    last_dos_from: Optional[date] = None
    last_dos_to: Optional[date] = None
    min_balance: Optional[float] = None


class SelfPayPatient(BaseModel):
    patient_id: int
    firstname: str
    lastname: str
    dob: date | None
    last_dos: date | None
    last_provider: str | None
    last_facility: str | None
    billed_total: Decimal
    patient_payments_total: Decimal
    patient_balance: Decimal
    
    model_config = ConfigDict(from_attributes=True)

class Pagination(BaseModel):
    page: int
    page_size: int
    total_rows: int
    total_pages: int

class SelfPayResponse(BaseModel):
    data: List[SelfPayPatient]
    pagination: Pagination