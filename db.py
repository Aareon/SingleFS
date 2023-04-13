from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, create_engine, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(length=255), unique=True, nullable=True)
    username = Column(String(length=32), unique=True, nullable=True)
    password = Column(String(length=255), unique=False, nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(length=255), unique=False, nullable=False)
    path = Column(String(length=255), unique=False, nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    pass_hash = Column(String(length=255), unique=False, nullable=False)
    file_size = Column(Integer, unique=False, nullable=False)


class Database:
    def __init__(self):
        self.engine = create_engine(
            "sqlite:///database.db?check_same_thread=False", echo=False
        )
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        Base.metadata.create_all(self.engine)
    
    def check_for_user(self, email=None, username=None):
        """Check if username or email exists already"""
        e = u = None
        if email is not None:
            e = self.session.query(User).filter_by(email=email).first()
        if username is not None:
            u = self.session.query(User).filter_by(username=username).first()
        if e or u:
            return True
        return False
    
    def create_new_user(self, email, username, pass_hash):
        """Create a new user. Password must be hashed"""
        new_user = User(email=email, username=username, password=pass_hash)
        self.session.add(new_user)
        self.session.commit()
