import os
import sys
sys.path.append(os.path.abspath(os.path.join(__file__, *[os.pardir] * 3)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'simplelms.settings'
import django
django.setup()

import csv
import json
from random import randint
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from lms_core.models import Course, CourseMember, CourseContent, Comment

import time
start_time = time.time()

filepath = './csv_data/'

with open(filepath+'user-data.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        obj_create = []
        for num, row in enumerate(reader):
            if not User.objects.filter(username=row['username']).exists():
                obj_create.append(User(username=row['username'], 
                                         password=make_password(row['password']), 
                                         email=row['email'],
                                         first_name=row['firstname'],
                                         last_name=row['lastname']))
        User.objects.bulk_create(obj_create)


with open(filepath+'course-data.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    obj_create = []
    for num,row in enumerate(reader):
        if not Course.objects.filter(pk=num+1).exists():
            obj_create.append(Course(name=row['name'], price=row['price'],
                                  description=row['description'], 
                                  teacher=User.objects.get(pk=int(row['teacher']))))
    Course.objects.bulk_create(obj_create)


with open(filepath+'member-data.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    obj_create = []
    for num, row in enumerate(reader):
        if not CourseMember.objects.filter(pk=num+1).exists():
            obj_create.append(CourseMember(course_id=Course.objects.get(pk=int(row['course_id'])),
                                        user_id=User.objects.get(pk=int(row['user_id'])), 
                                        roles=row['roles']))
    CourseMember.objects.bulk_create(obj_create)


with open(filepath+'contents.json') as jsonfile:
    comments = json.load(jsonfile)
    obj_create = []
    for num, row in enumerate(comments):
        if not CourseContent.objects.filter(pk=num+1).exists():
            obj_create.append(CourseContent(course_id=Course.objects.get(pk=int(row['course_id'])), 
                                         video_url=row['video_url'], name=row['name'], 
                                         description=row['description']))
    CourseContent.objects.bulk_create(obj_create)


with open(filepath+'comments.json') as jsonfile:
    comments = json.load(jsonfile)
    obj_create = []
    for num, row in enumerate(comments):
        if int(row['user_id']) > 50:
            row['user_id'] = randint(5, 40)
        if not Comment.objects.filter(pk=num+1).exists():
            obj_create.append(Comment(content_id=CourseContent.objects.get(pk=int(row['content_id'])), 
                                   member_id=User.objects.get(pk=int(row['user_id'])), 
                                   comment=row['comment']))
    Comment.objects.bulk_create(obj_create)

print("--- %s seconds ---" % (time.time() - start_time))