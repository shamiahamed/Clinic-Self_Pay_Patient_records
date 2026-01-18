import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# 1. You MUST call this to load the variables from your .env file
load_dotenv()

# 2. Get variables from .env
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")  # Changed from DB_PASS to match your .env
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT", "3306")
dbname = os.getenv("DB_NAME")

# 3. Safely encode the password in case it has special characters
safe_password = quote_plus(password) if password else ""

# 4. Construct the URL
DATABASE_URL = f"mysql+aiomysql://{user}:{safe_password}@{host}:{port}/{dbname}"

engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    pool_recycle=1800,
   # echo=True  # Turn this on to see the actual SQL being sent to the remote server
)

# Use async_sessionmaker (the modern SQLAlchemy 2.0 way)
AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session