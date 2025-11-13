from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from cheese.enums import PackagingType
from database import Base


class DBCheeseType(Base):
    __tablename__ = "cheese_type"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(511), nullable=False)
    cheese: Mapped[list["DBCheese"]] = relationship(back_populates="cheese_type")


class DBCheese(Base):
    __tablename__ = "cheese"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    price: Mapped[int]
    packaging_type: Mapped[PackagingType]
    cheese_type_id: Mapped[int] = mapped_column(ForeignKey("cheese_type.id"))
    cheese_type: Mapped["DBCheeseType"] = relationship(back_populates="cheese")
