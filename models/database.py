import time
import bcrypt
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, index=True, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    summary = Column(String)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    reg_date = Column(DateTime, default=time.asctime())
    is_verified = Column(Boolean, default=False)
    role = Column(Integer, default=0)

    def get_limited_info(self) -> dict:
        return {
            "name": self.name,
            "surname": self.surname,
            "summary": self.summary,
            "email": self.email,
            "reg_date": self.reg_date.timestamp(),
            "is_verified": self.is_verified,
            "role": self.role,
        }

    @staticmethod
    def password_hash(password):
        hash_pass = bcrypt.hashpw(password=password.encode('utf-8'), salt=bcrypt.gensalt())
        return hash_pass.decode('utf-8')

    def is_password_valid(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))


class Campaigns(Base):
    __tablename__ = "campaigns"
    __table_args__ = {'extend_existing': True}

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    campaign_id = Column(BIGINT)  # Duplicate values in the CSV can not be a primary key
    structure_value = Column(VARCHAR)
    status = Column(VARCHAR)


class AddGroups(Base):
    __tablename__ = "adgroups"
    __table_args__ = {'extend_existing': True}

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    ad_group_id = Column(BIGINT)  # Duplicate values in the CSV can not be a primary key as should
    campaign_id = Column(BIGINT)  # Duplicate values in the CSV can not be a foreign key Campaigns.campaign_id as should
    alias = Column(TEXT)
    status = Column(VARCHAR)


class SearchItems(Base):
    __tablename__ = "search_terms"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, index=True, primary_key=True)
    date = Column(Date)
    ad_group_id = Column(BIGINT)  # Duplicate values in the CSV can not be a foreign key AddGroups.ad_group_id as should
    campaign_id = Column(BIGINT)  # Duplicate values in the CSV can not be a foreign key Campaigns.campaign_id as should
    clicks = Column(INTEGER, default=0)
    cost = Column(FLOAT, default=0.0)
    conversion_value = Column(INTEGER, default=0)
    conversions = Column(INTEGER, default=0)
    search_term = Column(VARCHAR)


class Sessions(Base):
    __tablename__ = "sessions"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, index=True, primary_key=True)
    user_id = Column(Integer)
    access_token = Column(String)
    created_on = Column(Integer)
    expires_on = Column(Integer)
