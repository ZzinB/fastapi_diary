from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True) # 이메일 (로그인 시 사용)
    password = Column(String) #비밀번호
    nickname = Column(String)  #닉네임
    name = Column(String)  #이름
    phone = Column(String) #전화번호
    last_login = Column(DateTime, default=func.now()) #마지막 로그인
    is_staff = Column(Boolean, default=False) #스태프 여부
    is_admin = Column(Boolean, default=False) #관리자 여부
    is_active = Column(Boolean, default=False) #계정 활성화 여부

    diaries = relationship('Diary', back_populates='user')

class Diary(Base):
    __tablename__ = 'diaries'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id')) # 유저 정보
    title = Column(String) # 제목
    content = Column(Text)  # 내용
    mood = Column(String)  # 기분 (기쁨, 슬픔, 분노, 피곤, 짜증, 무난)
    tags = Column(String) # 태그
    created_at = Column(DateTime, default=func.now()) # 작성일자
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now()) # 수정일자

    user = relationship('User', back_populates='diaries')

User.diaries = relationship('Diary', back_populates='user')

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer ,primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True) #태그명

    diary_tags = relationship('DiaryTag', back_populates='tag')


class DiaryTag(Base):
    __tablename__ = 'diaries_tags'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    diary_id = Column(Integer, ForeignKey('diaries.id'), primary_key=True)  #일기 ID
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)  #태그 ID

    diary = relationship('Diary', back_populates='diary_tags')
    tag = relationship('Tag', back_populates='diary_tags')

# Diary와 Tag 간의 관계 (N:M)
Diary.diary_tags = relationship('DiaryTag', back_populates='diary')
Tag.diary_tags = relationship('DiaryTag', back_populates='tag')

# Analysis 테이블
class Analysis(Base):
    __tablename__ = 'analysis'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    target = Column(String)  # 태그/일기횟수
    period = Column(String)  # 일간/주간/월간/연간
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    description = Column(Text)
    result_image = Column(String)  # 분석 결과 이미지
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    user = relationship('User', back_populates='analysis')

# User와 Analysis 간의 관계 (1:N)
User.analysis = relationship('Analysis', back_populates='user')

# Notifications 테이블
class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    message = Column(Text)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())

    user = relationship('User', back_populates='notifications')

# User와 Notification 간의 관계 (1:N)
User.notifications = relationship('Notification', back_populates='user')