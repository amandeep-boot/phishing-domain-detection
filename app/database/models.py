from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.database.database import Base

class User(Base):
    """User model for authentication"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

class URLCheck(Base):
    """Store URL check history"""
    __tablename__ = "url_checks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=True)
    url = Column(Text, nullable=False)
    is_phishing = Column(Boolean, nullable=False)
    confidence = Column(Float, nullable=False)
    phishing_probability = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False)
    checked_at = Column(DateTime(timezone=True), server_default=func.now())

class ReportedURL(Base):
    """User-reported phishing URLs for model improvement"""
    __tablename__ = "reported_urls"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=True)
    url = Column(Text, nullable=False)
    is_phishing = Column(Boolean, nullable=False)
    reported_at = Column(DateTime(timezone=True), server_default=func.now())
