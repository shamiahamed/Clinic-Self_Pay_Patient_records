from sqlalchemy import Column, Integer, String, Date, DateTime, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Patient(Base):
    __tablename__ = "PATIENT"

    patient_id = Column("PATIENT_ID", Integer, primary_key=True, autoincrement=True)
    clinic_id = Column("CLINIC_ID", Integer, nullable=False)
    firstname = Column("FIRST_NAME", String(100))
    lastname = Column("LAST_NAME", String(100))
    dob = Column("DOB", DateTime)
    last_dos = Column("LAST_DOS", Date)
    provider_name = Column("PROVIDER_NAME", String(255))
    facility_name = Column("FACILITY_NAME", String(255))
    mark_as_delete = Column("MARK_AS_DELETE", Boolean, default=False)

class Claim(Base):
    __tablename__ = "CLAIM"

    claim_id = Column("CLAIM_ID", Integer, primary_key=True, autoincrement=True)
    patient_id = Column("PATIENT_ID", Integer, ForeignKey("PATIENT.PATIENT_ID"))
    clinic_id = Column("CLINIC_ID", Integer, nullable=False)
    visit_id = Column("VISIT_ID", Integer)
    billed = Column("BILLED", Numeric(10, 2), default=0.00)
    primary_payer_id = Column("PRIMARY_PAYER_ID", Integer, default=0)
    primary_payer_name = Column("PRIMARY_PAYER_NAME", String(100), default="SELF PAY")
    mark_as_delete = Column("MARK_AS_DELETE", Boolean, default=False)

class Payment(Base):
    __tablename__ = "PAYMENT"

    payment_id = Column("PAYMENT_ID", Integer, primary_key=True, autoincrement=True)
    clinic_id = Column("CLINIC_ID", Integer, nullable=False)
    visit_id = Column("VISIT_ID", Integer)
    amount = Column("AMOUNT", Numeric(10, 2), default=0.00)
    payer_type = Column("PAYER_TYPE", Integer)  # Your logic uses type 3
    mark_as_delete = Column("MARK_AS_DELETE", Boolean, default=False)