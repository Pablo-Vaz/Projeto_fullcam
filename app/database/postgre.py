import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.models.camera_model import Base

load_dotenv()

DATABASE = os.getenv("BANCO_POSTGRES")

conexao = create_async_engine(DATABASE, echo=True)

AsyncSessionLocal = async_sessionmaker(
    conexao, class_=AsyncSession, expire_on_commit=False
)


async def init_db():
    from app.models.camera_model import Camera

    async with conexao.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
