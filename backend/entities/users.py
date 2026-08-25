from sqlalchemy import Column, Integer, String
from connections.database import Base

class User(Base):
    """
    Entity representing a user in the database.
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, nullable=False)
    registration = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    period = Column(Integer)
    workload = Column(Integer)
    status = Column(String)