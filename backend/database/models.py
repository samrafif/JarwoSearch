from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.database.connection import db

class Document(db.Model):
    __tablename__ = "documents"

    id = Column(String, primary_key=True)
    name = Column(String)
    upload_date = Column(String)
    is_embedded = Column(Boolean, default=False)

    def __init__(self, id, name, upload_date, is_embedded) -> None:
        self.id = id
        self.name = name
        self.upload_date = upload_date
        self.is_embedded = is_embedded
    
    def __repr__(self) -> str:
        return f"<Document {self.name}>"