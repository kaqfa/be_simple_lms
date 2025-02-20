from ninja import NinjaAPI, UploadedFile, File, Form
from ninja.responses import Response
from lms_core.schema import CourseSchemaOut, CourseMemberOut, CourseSchemaIn
from lms_core.schema import CourseContentMini, CourseContentFull
from lms_core.schema import CourseCommentOut, CourseCommentIn
from lms_core.models import Course, CourseMember, CourseContent, Comment
from ninja_simple_jwt.auth.views.api import mobile_auth_router
from ninja_simple_jwt.auth.ninja_auth import HttpJwtAuth
from ninja.pagination import paginate, PageNumberPagination

from django.contrib.auth.models import User

apiv1 = NinjaAPI()
apiv1.add_router("/auth/", mobile_auth_router)
apiAuth = HttpJwtAuth()

@apiv1.get("/hello")
def hello(request):
    return "Hello World"

# - paginate list_courses
@apiv1.get("/courses", response=list[CourseSchemaOut])
@paginate(PageNumberPagination, page_size=10)
def list_courses(request):
    courses = Course.objects.select_related('teacher').all()
    return courses

# - my courses
@apiv1.get("/mycourses", auth=apiAuth, response=list[CourseMemberOut])
def my_courses(request):
    user = User.objects.get(id=request.user.id)
    courses = CourseMember.objects.select_related('user_id', 'course_id').filter(user_id=user)
    return courses

# - create course
@apiv1.post("/courses", auth=apiAuth, response={201:CourseSchemaOut})
def create_course(request, data: Form[CourseSchemaIn], image: UploadedFile = File(None)):
    user = User.objects.get(id=request.user.id)
    course = Course(
        name=data.name,
        description=data.description,
        price=data.price,
        image=image,
        teacher=user
    )

    if image:
        course.image.save(image.name, image)

    course.save()
    return 201, course

# - update course
@apiv1.post("/courses/{course_id}", auth=apiAuth, response=CourseSchemaOut)
def update_course(request, course_id: int, data: Form[CourseSchemaIn], image: UploadedFile = File(None)):
    if request.user.id != Course.objects.get(id=course_id).teacher.id:
        message = {"error": "Anda tidak diijinkan update course ini"}
        return Response(message, status=401)
    
    course = Course.objects.get(id=course_id)
    course.name = data.name
    course.description = data.description
    course.price = data.price
    if image:
        course.image.save(image.name, image)
    course.save()
    return course

# - detail course
@apiv1.get("/courses/{course_id}", response=CourseSchemaOut)
def detail_course(request, course_id: int):
    course = Course.objects.select_related('teacher').get(id=course_id)
    return course

# - list content course
@apiv1.get("/courses/{course_id}/contents", response=list[CourseContentMini])
def list_content_course(request, course_id: int):
    contents = CourseContent.objects.filter(course_id=course_id)
    return contents

# - detail content course
@apiv1.get("/courses/{course_id}/contents/{content_id}", response=CourseContentFull)
def detail_content_course(request, course_id: int, content_id: int):
    content = CourseContent.objects.get(id=content_id)
    return content

# - enroll course
@apiv1.post("/courses/{course_id}/enroll", auth=apiAuth, response=CourseMemberOut)
def enroll_course(request, course_id: int):
    user = User.objects.get(id=request.user.id)
    course = Course.objects.get(id=course_id)
    course_member = CourseMember(course_id=course, user_id=user, roles="std")
    course_member.save()
    # print(course_member)
    return course_member

# - list content comment
@apiv1.get("/contents/{content_id}/comments", auth=apiAuth, response=list[CourseCommentOut])
def list_content_comment(request, content_id: int):
    comments = CourseContent.objects.filter(course_id=content_id)
    return comments

# - create content comment
@apiv1.post("/contents/{content_id}/comments", auth=apiAuth, response={201: CourseCommentOut})
def create_content_comment(request, content_id: int, data: CourseCommentIn):
    user = User.objects.get(id=request.user.id)
    content = CourseContent.objects.get(id=content_id)

    if not content.course_id.is_member(user):
        message =  {"error": "You are not authorized to create comment in this content"}
        return Response(message, status=401)
    
    member = CourseMember.objects.get(course_id=content.course_id, user_id=user)
    
    comment = Comment(
        content_id=content,
        member_id=member,
        comment=data.comment
    )
    comment.save()
    return 201, comment

# - delete content comment
@apiv1.delete("/comments/{comment_id}", auth=apiAuth)
def delete_comment(request, comment_id: int):
    comment = Comment.objects.get(id=comment_id)
    if comment.member_id.user_id.id != request.user.id:
        return {"error": "You are not authorized to delete this comment"}
    comment.delete()
    return {"message": "Comment deleted"}   