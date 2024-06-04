from sqlalchemy import Column, Integer, Float, DateTime
from scr.database import Base
from datetime import datetime


class Roll(Base):
    __tablename__ = "rolls"
    id = Column(Integer, primary_key=True, nullable=False)
    length = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    date_added = Column(DateTime, default=datetime.now, nullable=False)
    date_removed = Column(DateTime, nullable=True)
