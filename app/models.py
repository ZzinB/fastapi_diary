import uuid
from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Users(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    nickname = Column(String)  # 닉네임
    name = Column(String)  # 이름
    phone = Column(String)  # 전화번호
    last_login = Column(DateTime, default=func.now())  # 마지막 로그인
    is_staff = Column(Boolean, default=False)  # 스태프 여부
    is_admin = Column(Boolean, default=False)  # 관리자 여부
    is_active = Column(Boolean, default=False)  # 계정 활성화 여부

    diaries = relationship('Diary', back_populates='user')
    analysis = relationship('Analysis', back_populates='user')
    notifications = relationship('Notification', back_populates='user')


class Diary(Base):
    __tablename__ = 'diaries'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String, ForeignKey('users.id'))  # 유저 정보 (UUID 타입으로 변경)
    title = Column(String)  # 제목
    content = Column(Text)  # 내용
    mood = Column(String)  # 기분 (기쁨, 슬픔, 분노, 피곤, 짜증, 무난)
    tags = Column(String)  # 태그
    created_at = Column(DateTime, default=func.now())  # 작성일자
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # 수정일자

    user = relationship('Users', back_populates='diaries')
    diary_tags = relationship('DiaryTag', back_populates='diary')


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)  # 태그명

    diary_tags = relationship('DiaryTag', back_populates='tag')


class DiaryTag(Base):
    __tablename__ = 'diaries_tags'

    diary_id = Column(Integer, ForeignKey('diaries.id'), primary_key=True)  # 일기 ID
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)  # 태그 ID

    diary = relationship('Diary', back_populates='diary_tags')
    tag = relationship('Tag', back_populates='diary_tags')


class Analysis(Base):
    __tablename__ = 'analysis'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String, ForeignKey('users.id'))  # UUID 타입으로 변경
    target = Column(String)  # 태그/일기횟수
    period = Column(String)  # 일간/주간/월간/연간
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    description = Column(Text)
    result_image = Column(String)  # 분석 결과 이미지
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    user = relationship('Users', back_populates='analysis')


class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String, ForeignKey('users.id'))  # UUID 타입으로 변경
    message = Column(Text)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())

    user = relationship('Users', back_populates='notifications')
