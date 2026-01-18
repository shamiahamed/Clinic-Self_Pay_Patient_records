import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT", "3306")
dbname = os.getenv("DB_NAME")

safe_password = quote_plus(password) if password else ""

# Construct the URL
DATABASE_URL = f"mysql+aiomysql://{user}:{safe_password}@{host}:{port}/{dbname}"

# SSL Configuration - Path to your cacert.pem
# Make sure this file is in your project folder
ssl_args = {
    "ssl": {
        "ca": os.path.join(os.getcwd(), "cacert.pem") 
    }
}

engine = create_async_engine(
    DATABASE_URL,
    connect_args=ssl_args, # Pass the SSL arguments here
    pool_size=20,
    max_overflow=40,
    pool_recycle=1800,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session