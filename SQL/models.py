
__all__ = ['Student', 'Group', 'Course']

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Table
from sqlalchemy import Integer, String
from sqlalchemy import ForeignKey


Base = declarative_base()

association_student_course = Table(
    "association_student_course",
    Base.metadata,
    Column("student", ForeignKey("Students.id")),
    Column("course", ForeignKey("Courses.id")),
)

association_student_group = Table(
    "association_student_group",
    Base.metadata,
    Column("student", ForeignKey("Students.id")),
    Column("group", ForeignKey("Groups.id")),
)


class Student(Base):
    __tablename__ = 'Students'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    group = relationship('Group', secondary=association_student_group)
    courses = relationship('Course', secondary=association_student_course)

    def __repr__(self):
        return f"{self.id}: {self.name} {self.surname} {self.group} {self.courses}"


class Group(Base):
    __tablename__ = 'Groups'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"{self.id}: {self.name}"


class Course(Base):
    __tablename__ = 'Courses'

    id = Column(Integer, primary_key=True)
    course_name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    def __repr__(self):
        return f"{self.id}: {self.course_name}"

