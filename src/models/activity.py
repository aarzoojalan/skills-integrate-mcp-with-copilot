from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from . import Base

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    time = Column(String(255), nullable=False)
    category = Column(String(100))  # Added for future filtering capability
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        """Convert the activity to a dictionary format"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "time": self.time,
            "category": self.category
        }