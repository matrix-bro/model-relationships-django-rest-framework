from django.contrib import admin

from app.models import Author, Book, Course, CourseStudent, Passport, Person, Student


admin.site.register(Person)
admin.site.register(Passport)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(CourseStudent)