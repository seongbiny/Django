from django.db import models

class Doctor(models.Model):
    name = models.TextField()

    def __str__(self):
        return f'{self.pk}번 의사 {self.name}'


class Patient(models.Model):
    name = models.TextField()
    # ManyToManyField - related_name 작성
    doctors = models.ManyToManyField(Doctor, through='Reservation', related_name='patients')

    def __str__(self):
        return f'{self.pk}번 환자 {self.name}'


class Reservation(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.doctor_id}번 의사의 {self.patient_id}번 환자'


patient1 = Patient.objects.get(pk=1)

patient1.reservation_set.all()
# <QuerySet [<Reservation: 1번 의사의 1번 환자>]>

patient1.doctors.all()
# <QuerySet [<Doctor: 1번 의사 justin>]>


doctor1 = Doctor.objects.get(pk=1)

doctor1.patient_set.all()
# AttributeError: 'Doctor' object has no attribute 'patient_set'

doctor1.patients.all()
# <QuerySet [<Patient: 1번 환자 tony>, <Patient: 2번 환자 harry>]>
