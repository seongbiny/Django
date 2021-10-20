from django.db import models

class Doctor(models.Model):
    name = models.TextField()

    def __str__(self):
        return f'{self.pk}번 의사 {self.name}'


class Patient(models.Model):
    name = models.TextField()
    # through option 삭제
    doctors = models.ManyToManyField(Doctor, related_name='patients')

    def __str__(self):
        return f'{self.pk}번 환자 {self.name}'
