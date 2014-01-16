from sqlalchemy import (Column, ForeignKey, Integer, String, Boolean, DateTime,
                        create_engine, and_)
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

engine = create_engine('sqlite:///db.sqlite')
Session = sessionmaker(bind=engine)
session = Session()


class Student(Base):
    """ Class for students DBO """

    __tablename__ = 'student'

    net_id = Column(String, primary_key=True)
    is_admin = Column(Boolean)

    @classmethod
    def get_submitted_assignments(cls, net_id):
        assignments = session.query(Assignment).join(Submission).filter(
            Submission.net_id == net_id
        )
        return assignments

    @classmethod
    def get_unsubmitted_assignments(cls, net_id):
        assignments = session.query(Assignment).join(Submission).filter(
            ~Assignment.id.in_(
                session.query(Assignment.id).join(Submission).filter(
                    Submission.net_id == net_id
                )
            )
        )
        return assignments




class Assignment(Base):
    """ Class for assignments DBO """

    __tablename__ = 'assignment'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(50))
    due_date = Column(DateTime)
    points = Column(Integer)
    active = Column(Boolean)


class Submission(Base):

    __tablename__ = 'submission'

    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey('assignment.id'))
    assignment = relationship('Assignment', uselist=False,
                              backref='submissions')
    net_id = Column(String(50), ForeignKey('student.net_id'))
    student = relationship('Student', uselist=False,
                           backref='submissions')
    submitted = Column(DateTime)
    score = Column(Integer)
    is_final = Column(Boolean)

Base.metadata.create_all(engine)

# test stuff
njordan = Student(net_id="njordan", is_admin=True)
bob = Student(net_id="bob", is_admin=False)
susan = Student(net_id="susan", is_admin=False)

session.add(njordan)
session.add(bob)
session.add(susan)

assignment1 = Assignment(name="Assignment 1", description="Stacks", due_date=datetime.datetime.now(), points=10, active=True)
assignment2 = Assignment(name="Assignment 2", description="Linked Lists", due_date=datetime.datetime.now(), points=10, active=True)

session.add(assignment1)
session.add(assignment2)

bob_submission1 = Submission(assignment=assignment1, student=bob, score=8, submitted=datetime.datetime.now())
bob_submission2 = Submission(assignment=assignment2, student=bob, score=7, submitted=datetime.datetime.now())

session.add(bob_submission1)
session.add(bob_submission2)
