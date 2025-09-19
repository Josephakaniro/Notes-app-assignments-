import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

Base = declarative_base()


class Format(PyEnum):
    TEXT = "txt"
    CSV = "csv"
    JSON = "json"


class Folder(Base):
    __tablename__ = "folders"

    id = Column(Integer, primary_key=True)
    folder_name = Column(String, nullable=False)
    tag = Column(String, nullable=True, default="None")
    amount_of_notes = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
    notes = relationship("Note", back_populates="folder")


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    folder_name = Column(String, ForeignKey("folders.folder_name"), nullable=False)
    title = Column(String, nullable=False)
    format = Column(Enum(Format), nullable=False, default=Format.TEXT)
    body = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    folder = relationship("Folder", back_populates="notes")
