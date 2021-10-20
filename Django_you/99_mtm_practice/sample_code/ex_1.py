from django.db import models

class Doctor(models.Model):
    name = models.TextField()

    def __str__(self):
        return f'{self.pk}번 의사 {self.name}'


class Patient(models.Model):
    name = models.TextField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pk}번 환자 {self.name}'


doctor1 = Doctor.objects.create(name='justin')
doctor2 = Doctor.objects.create(name='eric')
patient1 = Patient.objects.create(name='tony', doctor=doctor1)
patient2 = Patient.objects.create(name='harry', doctor=doctor2)
