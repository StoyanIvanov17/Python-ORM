from datetime import date

from django.db import models

# Create your models here.


class Lecturer(models.Model):
    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100
    )


class Subject(models.Model):
    name = models.CharField(
        max_length=100
    )

    code = models.CharField(
        max_length=10
    )

    lecturer = models.ForeignKey(
        to=Lecturer,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return f"The lecturer for {self.name} is {Lecturer.first_name} {Lecturer.last_name}."


class Student(models.Model):
    student_id = models.CharField(
        max_length=10,
        primary_key=True
    )

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100
    )

    birth_date = models.DateField()

    email = models.EmailField(
        unique=True
    )

    subjects = models.ManyToManyField(Subject, through='StudentEnrollment')


class StudentEnrollment(models.Model):
    class Grade(models.TextChoices):
        A = 'A'
        B = 'B'
        C = 'C'
        D = 'D'
        F = 'F'

    student = models.ForeignKey(
        to=Student,
        on_delete=models.CASCADE
    )

    subject = models.ForeignKey(
        to=Subject,
        on_delete=models.CASCADE
    )

    enrollment_date = models.DateField(
        default=date.today
    )

    grade = models.CharField(
        max_length=1,
        choices=Grade.choices
    )

    def __str__(self):
        return f"{Student.first_name} {Student.last_name} is enrolled in {self.subject}."


class LecturerProfile(models.Model):
    lecturer = models.OneToOneField(
        to=Lecturer,
        on_delete=models.CASCADE
    )

    email = models.EmailField(
        unique=True
    )

    bio = models.TextField(
        blank=True,
        null=True
    )

    office_location = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
