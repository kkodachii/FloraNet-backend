from django.db import models
from django.contrib.auth.models import AbstractUser

# Optional: extend user model if needed
class User(AbstractUser):
    name = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=20)
    house = models.ForeignKey('House', on_delete=models.SET_NULL, null=True, blank=True, related_name='residents')
    resident_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class House(models.Model):
    house_number = models.CharField(max_length=50)
    block_lot = models.CharField(max_length=50)
    street = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.house_number}, {self.block_lot}, {self.street}'


class Vendor(models.Model):
    resident = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vendors')
    business_name = models.CharField(max_length=255)

    def __str__(self):
        return self.business_name


class VehiclePass(models.Model):
    resident = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicle_passes')
    vehicle_pass_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    mode_of_payment = models.CharField(max_length=50)
    vehicle_model = models.CharField(max_length=100)
    plate_number = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.plate_number} - {self.vehicle_pass_id}'


class Alert(models.Model):
    resident = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alerts')
    reported_at = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(max_length=50)
    notified_party = models.CharField(max_length=100)

    def __str__(self):
        return f'Alert from {self.resident.name} on {self.reported_at}'


class CCTVRequest(models.Model):
    resident = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cctv_requests')
    requested_at = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(max_length=50)
    notified_party = models.CharField(max_length=100)

    def __str__(self):
        return f'CCTV Request by {self.resident.name} on {self.requested_at}'


class MonthlyDue(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='monthly_dues')
    resident = models.ForeignKey(User, on_delete=models.CASCADE, related_name='monthly_dues')
    due_month = models.DateField(help_text="Use the first day of the month to represent it.")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.house} - {self.due_month.strftime("%B %Y")}'


class Payment(models.Model):
    resident = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    method_of_payment = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField()

    def __str__(self):
        return f'{self.resident.name} - {self.amount} on {self.paid_at}'


class Complaint(models.Model):
    COMPLAINT_TYPES = (
        ('general', 'General'),
        ('service', 'Service'),
    )

    resident = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    complaint_type = models.CharField(max_length=20, choices=COMPLAINT_TYPES)
    complained_at = models.DateTimeField()
    service_type = models.CharField(max_length=100)
    trigger_type = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f'{self.complaint_type} complaint by {self.resident.name}'
