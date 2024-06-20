from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .connection import db

class Document(db.Model):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    upload_date = Column(String)
    is_embedded = Column(Boolean, default=False)