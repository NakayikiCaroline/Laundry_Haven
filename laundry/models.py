from django.db import models
from django.utils import timezone


class Customer(models.Model):
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.full_name


class Service(models.Model):
    service_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.service_name


class LaundryOrder(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Ready', 'Ready for Pickup'),
        ('Completed', 'Completed'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    order_date = models.DateTimeField(auto_now_add=True)

    pickup_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.full_name}"


class Payment(models.Model):

    PAYMENT_METHODS = [
        ('Cash', 'Cash'),
        ('Mobile Money', 'Mobile Money'),
        ('Bank', 'Bank Transfer'),
        ('Card', 'Card'),
    ]

    order = models.OneToOneField(
        LaundryOrder,
        on_delete=models.CASCADE
    )

    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS
    )

    payment_date = models.DateTimeField(default=timezone.now)

    reference = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    paid = models.BooleanField(default=True)

    def __init__(self, *args, **kwargs):
        amount = kwargs.pop('amount', None)
        if amount is not None and 'amount_paid' not in kwargs:
            kwargs['amount_paid'] = amount
        super().__init__(*args, **kwargs)

    @property
    def amount(self):
        return self.amount_paid

    @amount.setter
    def amount(self, value):
        self.amount_paid = value

    def __str__(self):
        return f"Payment #{self.id}"


class Employee(models.Model):

    first_name = models.CharField(max_length=50)

    last_name = models.CharField(max_length=50)

    phone = models.CharField(max_length=20)

    position = models.CharField(max_length=50)

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class BusinessInformation(models.Model):
    business_name = models.CharField(
        max_length=150,
        default="Laundry Haven"
    )
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    receipt_footer = models.CharField(
        max_length=200,
        blank=True,
        default="Thank you for choosing Laundry Haven!"
    )

    def __str__(self):
        return self.business_name    