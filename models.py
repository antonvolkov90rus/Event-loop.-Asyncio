import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer

# ← Читаем .env
from dotenv import load_dotenv
load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "app")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")  # ← для запуска НА ХОСТЕ (Windows)
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")      # ← на хосте — 5432 (если ports: 5432:5432)

POSTGRES_DSN = (
    f"postgresql+asyncpg://"
    f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/"
    f"{POSTGRES_DB}"
)

engine = create_async_engine(POSTGRES_DSN, echo=False)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase, AsyncAttrs):
    pass

class Character(Base):
    __tablename__ = "characters"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    birth_year: Mapped[str] = mapped_column(String(100))
    eye_color: Mapped[str] = mapped_column(String(100))
    films: Mapped[str] = mapped_column(String(500))
    gender: Mapped[str] = mapped_column(String(50))
    hair_color: Mapped[str] = mapped_column(String(100))
    height: Mapped[str] = mapped_column(String(10))
    homeworld: Mapped[str] = mapped_column(String(100))
    mass: Mapped[str] = mapped_column(String(10))
    name: Mapped[str] = mapped_column(String(100))
    skin_color: Mapped[str] = mapped_column(String(100))
    species: Mapped[str] = mapped_column(String(500))
    starships: Mapped[str] = mapped_column(String(500))
    vehicles: Mapped[str] = mapped_column(String(500))

async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_orm():
    await engine.dispose()