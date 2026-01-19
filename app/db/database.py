import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# Force reload to ensure it clears old cached values
load_dotenv(override=True) 

# Requirement #1: Load only the single DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")

# DEBUG PRINT: This will show you EXACTLY what IP is being used in your terminal
print(f"\n--- DEBUG: APP IS CONNECTING TO: {DATABASE_URL} ---\n")

engine = create_async_engine(
    DATABASE_URL,
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
        try:
            yield session
        finally:
            await session.close()

















































# import os
# from dotenv import load_dotenv
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# # 1. You MUST call this to load the variables from your .env file
# load_dotenv()

# # 2. Get variables from .env
# user = os.getenv("DB_USER")
# password = os.getenv("DB_PASSWORD")  # Changed from DB_PASS to match your .env
# host = os.getenv("DB_HOST")
# port = os.getenv("DB_PORT", "3306")
# dbname = os.getenv("DB_NAME")


# # 4. Construct the URL
# # DATABASE_URL = f"mysql+aiomysql://{user}:{safe_password}@{host}:{port}/{dbname}"
# DATABASE_URL = os.getenv("DATABASE_URL")

# engine = create_async_engine(
#     DATABASE_URL,
#     pool_size=20,
#     max_overflow=40,
#     pool_recycle=1800,
#    # echo=True  # Turn this on to see the actual SQL being sent to the remote server
# )

# # Use async_sessionmaker 
# AsyncSessionLocal = async_sessionmaker(
#     bind=engine, 
#     class_=AsyncSession, 
#     expire_on_commit=False
# )

# async def get_db():
#     async with AsyncSessionLocal() as session:
#         yield session