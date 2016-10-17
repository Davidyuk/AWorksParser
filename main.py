import sys
import requests

from parsers import groups_parser, student_list_parser, student_parser
from models import Student, Group, Discipline, Task, Mark

baseUrl = 'http://imcs.dvfu.ru/works/'
session = requests.Session()

groups = list(map(lambda x: Group.create_or_get(**x)[0], groups_parser(session.get(baseUrl + 'students').content)))
print('Found {} groups'.format(len(groups)))

for group in groups:
    data = {'group': group.id, 'student_name': '', 'do_select': 'Выбрать'}
    students = list(map(lambda x: Student.create_or_get(**x)[0].groups.add(group),
                        student_list_parser(session.post(baseUrl + 'students', data=data).content)))
    sys.stdout.write('\rFound {} students in {}'.format(len(students), group.name))

students = Student.select()
sys.stdout.write('\rFound {} students\n'.format(len(students)))

count = 0
for student in students:
    for disciplineDict in student_parser(session.get(baseUrl + 'marks_student?id={}'.format(student.id)).content):
        tasks = disciplineDict.pop('tasks')
        (discipline, _) = Discipline.create_or_get(**disciplineDict)
        for taskDict in tasks:
            marks = taskDict.pop('marks')
            (task, _) = Task.create_or_get(**taskDict, discipline=discipline)
            for mark in marks:
                Mark.create_or_get(**mark, task=task, student=student)
    count += 1
    sys.stdout.write('\rProcessed {}/{} students'.format(count, len(students)))

print('\nFinished')
