from sqlalchemy import (Column, ForeignKey, Integer, String, Boolean, DateTime,
                        create_engine, and_, func)
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

engine = create_engine('sqlite:///app.db')
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
        assignments = session.query(Assignment).join(Submission).filter(and_(
            ~Assignment.id.in_(
                session.query(Assignment.id).join(Submission).filter(
                    Submission.net_id == net_id
                )
            ),
            Submission.is_final
        )
        )
        return assignments

    @classmethod
    def get_assignment_submissions(cls, net_id, assignment_id):
        submissions = session.query(Submission).filter(and_(
            Assignment.id == assignment_id,
            Submission.net_id == net_id
        ))
        print submissions
        for row in submissions:
            print row
        return submissions

    @classmethod
    def check_assignment_finalized(cls, net_id, assignment_id):
        count = session.query(func.count(Submission.id)).filter(and_(
            Assignment.id == assignment_id,
            Submission.is_final == True,
            Submission.net_id == net_id
        )).scalar()
        print count
        return count


class Assignment(Base):
    """ Class for assignments DBO """

    __tablename__ = 'assignment'

    @classmethod
    def get_active_assignment_by_id(cls, assignment_id):
        assignment = session.query(Assignment).get(assignment_id)
        return assignment

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(50))
    long_description = Column(String(500))
    due_date = Column(DateTime)
    points = Column(Integer)
    is_active = Column(Boolean)


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

class Resource(Base):

    __tablename__ = 'resource'

    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey('assignment.id'))
    assignment = relationship('Assignment', uselist=False, backref='resources')
    filename = Column(String(50))
    description = Column(String(100))

Base.metadata.create_all(engine)

# test stuff
njordan = Student(net_id="njordan", is_admin=True)
bob = Student(net_id="bob", is_admin=False)
susan = Student(net_id="susan", is_admin=False)

session.add(njordan)
session.add(bob)
session.add(susan)

assignment1 = Assignment(name="Assignment 1", description="Stacks", due_date=datetime.datetime.now(), points=10, is_active=True)
assignment2 = Assignment(name="Assignment 2", description="Linked Lists", due_date=datetime.datetime.now(), points=10, is_active=True)

session.add(assignment1)
session.add(assignment2)

resource1 = Resource(assignment=assignment1, filename="Makefile", description="the makefile brah")
resource2 = Resource(assignment=assignment1, filename="Stack.h", description="your stack header brah")

session.add(resource1)
session.add(resource2)

bob_submission1 = Submission(assignment=assignment1, student=bob, score=8, submitted=datetime.datetime.now(), is_final=False)
bob_submission2 = Submission(assignment=assignment1, student=bob, score=9, submitted=datetime.datetime.now(), is_final=True)
bob_submission3 = Submission(assignment=assignment2, student=bob, score=7, submitted=datetime.datetime.now(), is_final=True)
susan_submission1 = Submission(assignment=assignment1, student=susan, score=7, submitted=datetime.datetime.now(), is_final=False)
susan_submission2 = Submission(assignment=assignment1, student=susan, score=9, submitted=datetime.datetime.now(), is_final=False)

session.add(bob_submission1)
session.add(bob_submission2)
session.add(bob_submission3)
session.add(susan_submission1)
session.add(susan_submission2)

#session.commit()
