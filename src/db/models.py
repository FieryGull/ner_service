import uuid

from sqlalchemy import Column, ForeignKey, Text
from sqlalchemy_utils import EmailType
from sqlalchemy.dialects.postgresql import BYTEA, UUID
from sqlalchemy.orm import relationship

from src.db import Base


class User(Base):
    """
    Table for users info
    """
    __tablename__ = "User"
    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    email = Column(EmailType, nullable=False)
    hashed_password = Column(Text, nullable=False)

    reports = relationship("Report", cascade="all,delete-orphan", backref="owner")


class Report(Base):
    """
    Table for result reports storing
    """
    __tablename__ = "Report"
    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("User.id"), nullable=False)
    name = Column(Text)
    doc = Column(BYTEA)
