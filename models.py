from playhouse.sqlite_ext import SqliteExtDatabase
import peewee
from playhouse.fields import ManyToManyField

db = SqliteExtDatabase('aWorks.db')
db.connect()


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Student(BaseModel):
    name = peewee.CharField()


class Group(BaseModel):
    name = peewee.CharField()
    students = ManyToManyField(Student, related_name='groups')

StudentGroup = Group.students.get_through_model()


class Discipline(BaseModel):
    name = peewee.CharField(unique=True)


class Task(BaseModel):
    name = peewee.CharField()
    maxRate = peewee.IntegerField()
    rateWeight = peewee.IntegerField()
    discipline = peewee.ForeignKeyField(Discipline, related_name='tasks')
    date = peewee.DateTimeField()


class Mark(BaseModel):
    task = peewee.ForeignKeyField(Task, related_name='marks')
    student = peewee.ForeignKeyField(Student, related_name='marks')
    rate1 = peewee.FloatField()
    rate2 = peewee.FloatField(null=True)
    date = peewee.DateTimeField()

db.drop_tables([Student, Group, StudentGroup, Discipline, Task, Mark], safe=True)
db.create_tables([Student, Group, StudentGroup, Discipline, Task, Mark])
