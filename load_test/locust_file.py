from locust import HttpUser, TaskSet, task, between
import json

class UserBehavior(TaskSet):
    def on_start(self):
        self.login()

    def login(self):
        response = self.client.post("/auth/sign-in", json={
            "username": "LarissaWylie", 
            "password": "RLS71GOH8GF" 
        })
        if response.status_code == 200:
            self.token = response.json().get("access") 
        else:
            print("Login failed:", response.text)

    @task(1)
    def get_my_courses(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.get("/mycourses", headers=headers)
        if response.status_code == 200:
            self.courses = response.json() 
            # print("My Courses:", self.courses)
            if self.courses:
                self.course_id = self.courses[0]['course_id']['id']
                self.get_course_contents(self.course_id)

    def get_course_contents(self, course_id):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.get(f"/courses/{course_id}/contents", headers=headers)
        if response.status_code == 200:
            self.contents = response.json() 
            # print("Course Contents:", self.contents)
            if self.contents:
                self.content_id = self.contents[0]['id'] 
                self.post_comment(self.content_id)

    def post_comment(self, content_id):
        headers = {"Authorization": f"Bearer {self.token}"}
        comment_data = {"comment": "This is a test comment."}
        response = self.client.post(f"/contents/{content_id}/comments", json=comment_data, headers=headers)
        if response.status_code == 201:
            self.comment_id = response.json().get("id")
            # print("Comment posted:", response.json())
            self.delete_comment(self.comment_id)

    def delete_comment(self, comment_id):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.delete(f"/comments/{comment_id}", headers=headers)
        if response.status_code == 200:
            print("Comment deleted:", response.json())
        else:
            print("Failed to delete comment:", response.text)

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 2) 

