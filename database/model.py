import datetime

from sqlalchemy import BigInteger, VARCHAR, ForeignKey, DateTime, Boolean, Column, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


class UsersTable(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    username: Mapped[str] = mapped_column(VARCHAR)
    name: Mapped[str] = mapped_column(VARCHAR)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    join: Mapped[str] = mapped_column(VARCHAR, default=None, nullable=True)
    active: Mapped[int] = mapped_column(Integer, default=1)
    activity: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=False), default=func.now())
    entry: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=False), default=func.now())


class DiagnosticFormTable(Base):
    __tablename__ = 'diagnostic-form'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id', ondelete='CASCADE'))
    niche: Mapped[str] = mapped_column(String)
    pain: Mapped[str] = mapped_column(String)
    problem: Mapped[str] = mapped_column(String)
    digitalization: Mapped[str] = mapped_column(String)
    finance: Mapped[str] = mapped_column(String)
    purpose: Mapped[str] = mapped_column(String)


class ConsultFormTable(Base):
    __tablename__ = 'consult-form'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id', ondelete='CASCADE'))
    focus: Mapped[str] = mapped_column(String)
    process: Mapped[str] = mapped_column(String)
    deadline: Mapped[str] = mapped_column(String)
    features: Mapped[str] = mapped_column(String)
    criteria: Mapped[str] = mapped_column(String)


class DeeplinksTable(Base):
    __tablename__ = 'deeplinks'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    link: Mapped[str] = mapped_column(VARCHAR)
    entry: Mapped[int] = mapped_column(BigInteger, default=0)


class AdminsTable(Base):
    __tablename__ = 'admins'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(VARCHAR)


class OneTimeLinksIdsTable(Base):
    __tablename__ = 'links'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    link: Mapped[str] = mapped_column(VARCHAR)

