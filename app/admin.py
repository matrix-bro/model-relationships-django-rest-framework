from django.contrib import admin

from app.models import Passport, Person


admin.site.register(Person)
admin.site.register(Passport)