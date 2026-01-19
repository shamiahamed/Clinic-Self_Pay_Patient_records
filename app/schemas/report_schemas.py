from pydantic import BaseModel, ConfigDict, Field
from datetime import date
from decimal import Decimal
from typing import List, Optional

# --- REQUEST SCHEMA (The Filters) ---
class SelfPayFilter(BaseModel):
    clinic_id: int = Field(..., gt=0)
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=100) 
    search: Optional[str] = None
    dob_from: Optional[str] = None
    dob_to: Optional[str] = None
    last_dos_from: Optional[str] = None
    last_dos_to: Optional[str] = None
    min_balance: Optional[float] = 0.0
    sort_by: Optional[str] = "last_dos"
    sort_dir: Optional[str] = "desc"


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