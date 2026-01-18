from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.routes.report_controller import self_pay_controller
from app.logger.api_logger import log_execution
# Import both the Request and Response schemas
from app.schemas.report_schemas import SelfPayFilter, SelfPayResponse

router = APIRouter(prefix="/api/reports", tags=["Reports"])

@router.get("/self-pay-patients", response_model=SelfPayResponse)
@log_execution
async def get_self_pay_patients(
    filters: SelfPayFilter = Depends(), 
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Fetch self-pay patients report.
    Logic: Uses 'SelfPayFilter' for inputs and 'SelfPayResponse' for output.
    """
    # Clean and simple: Pass the database, user, and the filter object
    return await self_pay_controller(
        db=db,
        user=user,
        filters=filters
    )