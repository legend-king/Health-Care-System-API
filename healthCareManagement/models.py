from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Patient(models.Model):
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=20)
    username = models.CharField(max_length=50)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    dob = models.DateField()

class Doctor(models.Model):
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=20)
    username = models.CharField(max_length=50)
    specialist = models.IntegerField()
    consultation_charge = models.IntegerField()

class Driver(models.Model):
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=20)
    username = models.CharField(max_length=50)

class Nutritionist(models.Model):
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=20)
    username = models.CharField(max_length=50)
    consultation_charge = models.IntegerField()

class Specialist(models.Model):
    name = models.CharField(max_length=50)

class PhysicalActivity(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    calories_burned = models.IntegerField()

class Chat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_chats')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_chats')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Prescription(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    symptoms = models.TextField()
    diagnosis = models.TextField()

class PrescribedMedicine(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    medicine_name = models.CharField(max_length=500)
    medicine_type = models.CharField(max_length=50)
    before_breakfast = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    after_breakfast = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    before_lunch = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    after_lunch = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    before_dinner = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    evening = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    after_dinner = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    tablets = models.IntegerField(null=True)
    duration = models.IntegerField(null=True)

class PatientReport(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    report_type = models.CharField(max_length=255)
    file = models.FileField(upload_to='reports/')
