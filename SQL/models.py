
__all__ = ('Student', 'Group', 'Course', 'Base', 'student_course')

from sqlalchemy import Integer, String, ForeignKey, Column, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


student_course = Table(
    "student_course",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("Students.id")),
    Column("course_id", Integer, ForeignKey("Courses.id")),
)


class Student(Base):
    __tablename__ = 'Students'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)

    group = Column(Integer, ForeignKey('Groups.id'))

    courses = relationship('Course', secondary=student_course)

    def __repr__(self):
        return f"{self.id}:{self.name}:{self.surname}:{self.group}:{self.courses}"


class Group(Base):
    __tablename__ = 'Groups'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return f"{self.name}"


class Course(Base):
    __tablename__ = 'Courses'

    id = Column(Integer, primary_key=True)
    course_name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)

    def __repr__(self):
        return f"{self.course_name}"
