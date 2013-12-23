from sqlalchemy import (Column, ForeignKey, Integer,
                        String, Boolean, DateTime, create_engine)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

db = create_engine('sqlite:///db.sqlite')


class Student(Base):
    """ Class for students DBO """

    __tablename__ = 'student'

    net_id = Column(String, primary_key=True)
    is_admin = Column(Boolean)


class Assignment(Base):
    """ Class for assignments DBO """

    __tablename__ = 'assignment'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    due_date = Column(DateTime)
    points = Column(Integer)


class Submission(Base):

    __tablename__ = 'submission'

    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey('assignment.id'))
    net_id = Column(Integer, ForeignKey('student.net_id'))
    submitted = Column(DateTime)
    score = Column(Integer)

Base.metadata.create_all(db)
