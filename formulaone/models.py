from formulaone.extensions import db, login_manager
from sqlalchemy import Integer, String, Text, Table, Column, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    firstname: Mapped[str] = mapped_column(String(30), nullable=True)
    lastname: Mapped[str] = mapped_column(String(30), nullable=True)
    avatar: Mapped[str] = mapped_column(String(25), default="avatar.png")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    drivers: Mapped[List["FormulaOne"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"<User: {self.username}>"


formula_team = Table(
    "formula_team",
    db.metadata,
    Column("team_id", Integer, ForeignKey("team.id"), primary_key=True),
    Column("formulaone_id", Integer, ForeignKey("formulaone.id"), primary_key=True),
)


class Team(db.Model):
    __tablename__ = "team"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)

    drivers: Mapped[List["FormulaOne"]] = relationship(
        secondary=formula_team, back_populates="teams"
    )

    def __repr__(self):
        return f"<Team: {self.name}>"


class FormulaOne(db.Model):
    __tablename__ = "formulaone"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    number: Mapped[str] = mapped_column(String(20), nullable=False)
    world_championships: Mapped[str] = mapped_column(String(20), nullable=False)
    nationality: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(Text, nullable=False)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="drivers")

    teams: Mapped[List["Team"]] = relationship(
        secondary=formula_team, back_populates="drivers"
    )

    def __repr__(self):
        return f"<Driver: {self.name}>"