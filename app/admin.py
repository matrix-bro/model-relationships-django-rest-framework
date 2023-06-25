from django.contrib import admin

from app.models import Author, Book, Passport, Person


admin.site.register(Person)
admin.site.register(Passport)
admin.site.register(Author)
admin.site.register(Book)