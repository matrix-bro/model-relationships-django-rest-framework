from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Passport(models.Model):
    passport_no = models.CharField(max_length=20, unique=True)
    person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name="passport")

    def __str__(self):
        return self.passport_no