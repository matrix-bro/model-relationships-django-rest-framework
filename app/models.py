from django.db import models

# One to One with Person and Passport
class Person(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Passport(models.Model):
    passport_no = models.CharField(max_length=20, unique=True)
    person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name="passport")

    def __str__(self):
        return self.passport_no
    
# One to Many with Author and Book
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")

    def __str__(self):
        return self.title
    
# Many to Many with Course and Student    
class Course(models.Model):
    name = models.CharField(max_length=100)

class Student(models.Model):
    name = models.CharField(max_length=100)
    courses = models.ManyToManyField(Course, through="CourseStudent",
                                     related_name="students")
    # Using Intermediate table CourseStudent

class CourseStudent(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date_enrolled = models.DateField()

    class Meta:
        unique_together = ('student', 'course')
        # To prevent duplicate entries of student and course together