from sqlalchemy import (Column, ForeignKey, Integer, String, Boolean, DateTime,
                        create_engine, and_, func, create_engine)
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
import os

Base = declarative_base()
engine = create_engine('sqlite:///app.db')
db_session = scoped_session(sessionmaker(bind=engine))

class Student(Base):
    """ Class for students DBO """

    __tablename__ = 'student'

    net_id = Column(String, primary_key=True)
    is_admin = Column(Boolean)

    @classmethod
    def get_submitted_assignments(cls, net_id):
        assignments = db_session.query(Assignment).join(Submission).filter(
            Submission.net_id == net_id
        )
        return assignments

    @classmethod
    def get_unsubmitted_assignments(cls, net_id):
        assignments = db_session.query(Assignment).join(Submission).filter(and_(
            ~Assignment.id.in_(
                db_session.query(Assignment.id).join(Submission).filter(
                    Submission.net_id == net_id
                )
            ),
            Submission.is_final
        )
        )
        return assignments



class Assignment(Base):
    """ Class for assignments DBO """

    __tablename__ = 'assignment'

    @classmethod
    def get_active_assignment_by_id(cls, assignment_id):
        assignment = db_session.query(Assignment).get(assignment_id)
        return assignment

    @classmethod
    def check_assignment_completed(cls, net_id, assignment_id):
        count = db_session.query(func.count(Submission.id)).filter(and_(
            Submission.assignment_id == assignment_id,
            Submission.is_final
        )).scalar()
        return True if count > 0 else False

    @classmethod
    def get_assignment_submissions(cls, net_id, assignment_id):
        submissions = db_session.query(Submission).join(Assignment).filter(and_(
            Assignment.id == assignment_id,
            Submission.net_id == net_id
        ))
        return submissions

    @classmethod
    def get_assignment_resources(cls, assignment_id):
        resources = db_session.query(Resource).filter(
            Resource.assignment_id == assignment_id
        )
        return resources


    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(50))
    long_description = Column(String(500))
    due_date = Column(DateTime)
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
    filename = Column(String(50))
    submitted = Column(DateTime)
    is_final = Column(Boolean)
    build_output = Column(String(1000))

    @classmethod
    def create_submission(cls, assignment_id, net_id, filename, submitted, is_final):
        submission = Submission()
        submission.assignment_id = assignment_id
        submission.net_id = net_id
        submission.filename = filename
        submission.submitted = submitted
        submission.is_final = is_final
        db_session.add(submission)
        db_session.commit()
        db_session.refresh(submission)
        return submission.id

class Resource(Base):

    __tablename__ = 'resource'

    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey('assignment.id'))
    assignment = relationship('Assignment', uselist=False, backref='resources')
    filename = Column(String(50))
    description = Column(String(100))

class Test(Base):

    __tablename__ = 'test'

    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey('assignment.id'))
    assignment = relationship('Assignment', uselist=False, backref='tests')
    executable_filename = Column(String(50))
    test_type = Column(String(50))
    reference_executable_filename = Column(String(50))
    is_private = Column(Boolean)
    points = Column(Integer)

class SubmissionTest(Base):

    __tablename__ = 'submission_test'

    submission_id = Column(Integer, ForeignKey('submission.id'), primary_key=True)
    submission = relationship('Submission', uselist=False, backref='submission_tests')
    test_id = Column(Integer, ForeignKey('test.id'), primary_key=True)
    test = relationship('Test', uselist=False, backref='submission_tests')
    output = Column(String(1200))
    score = Column(Integer)

def test_data():
    # Clear existing database
    try:
        os.remove('app.db')
    except OSError:
        pass

    # Create Database
    Base.metadata.create_all(bind=engine)

    # Test Data
    njordan = Student(net_id="njordan", is_admin=True)
    bob = Student(net_id="bob", is_admin=False)
    susan = Student(net_id="susan", is_admin=False)

    db_session.add(njordan)
    db_session.add(bob)
    db_session.add(susan)

    assignment1 = Assignment(name="Assignment 1", description="Stacks", due_date=datetime.datetime.now(), is_active=True)
    assignment2 = Assignment(name="Assignment 2", description="Linked Lists", due_date=datetime.datetime.now(), is_active=True)

    db_session.add(assignment1)
    db_session.add(assignment2)

    resource1 = Resource(assignment=assignment1, filename="Makefile", description="the makefile brah")
    resource2 = Resource(assignment=assignment1, filename="Stack.h", description="your stack header brah")

    db_session.add(resource1)
    db_session.add(resource2)

    test1 = Test(assignment=assignment1, executable_filename="unit_tests_public", test_type="unit", is_private=False, points=10)
    test2 = Test(assignment=assignment1, executable_filename="unit_tests_private", test_type="unit", is_private=True, points=10)
    test3 = Test(assignment=assignment1, executable_filename="diff_test_1", test_type="diff", is_private=False, reference_executable_filename="diff_test_1_reference", points=10)
    test4 = Test(assignment=assignment1, executable_filename="diff_test_2", test_type="diff", is_private=False, reference_executable_filename="diff_test_2_reference", points=10)

    db_session.add(test1)
    db_session.add(test2)
    db_session.add(test3)
    db_session.add(test4)

    bob_submission1 = Submission(assignment=assignment1, student=bob, submitted=datetime.datetime.now(), is_final=False)
    bob_submission2 = Submission(assignment=assignment1, student=bob, submitted=datetime.datetime.now(), is_final=False)
    bob_submission3 = Submission(assignment=assignment2, student=bob, submitted=datetime.datetime.now(), is_final=True)
    susan_submission1 = Submission(assignment=assignment1, student=susan, submitted=datetime.datetime.now(), is_final=False)
    susan_submission2 = Submission(assignment=assignment1, student=susan, submitted=datetime.datetime.now(), is_final=False)

    db_session.add(bob_submission1)
    db_session.add(bob_submission2)
    db_session.add(bob_submission3)
    db_session.add(susan_submission1)
    db_session.add(susan_submission2)

    db_session.commit()
