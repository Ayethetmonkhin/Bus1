from django.db import models
from .models import *
from django.contrib.auth.models import User
# Create your models here.

class Passenger(models.Model):
    Passenger_name = models.CharField(max_length=100)
    NRC = models.CharField(max_length=50, unique=True)
    Passenger_phno = models.CharField(max_length=50)

    def __str__(self):
        return self.Passenger_name
    
    
class BusOperator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null= True)
    Bus_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.Bus_name
    

class Route(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null= True)
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    fare = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.from_location} to {self.to_location}"

class Bus(models.Model):
    BUS_TYPE_CHOICES = [
        ('vip', 'VIP'), 
        ('normal', 'Normal'),]
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null= True)
    operator = models.ForeignKey(BusOperator, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, blank=True, null=True)
    bus_type = models.CharField(max_length=50, choices=BUS_TYPE_CHOICES, default='normal', blank = True, null=True)  # e.g., VIP, Normal
    driver_name = models.CharField(max_length=100)
    driver_phone = models.CharField(max_length=15)
    bus_number = models.CharField(max_length=50, blank=True, null=True)  # unique bus  code
    departure_date = models.DateField(blank=True, null= True)
    departure_time = models.TimeField(blank=True, null= True)
    
    def __str__(self):
        return self.bus_number
    
class BusRoute(models.Model):
    route =models.ForeignKey(Route, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    from_location = models.CharField(max_length=100, blank=True, null=True)
    to_location = models.CharField(max_length=100, blank=True, null=True)
    price = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    path = models.TextField(blank=True, null=True)

    def __str__(self):
         return f"{self.bus} - {self.route}"
    
class Seat(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=5)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.seat_number}"

    
class Price(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    seat_type = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.route} - {self.seat_type}: {self.amount} Ks"
    
    
class Booking(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, default='Pending')  # Pending, Confirmed, Cancelled

    def __str__(self):
        return f"Booking for {self.passenger} on {self.date}"

#don't use
class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    method = models.CharField(max_length=20)  # e.g., Kpay, Wavepay
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=100, null=True, blank=True)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.method} - {self.amount} Ks"
    
#don't use
class Ticket(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    ticket_number = models.CharField(max_length=100, unique=True)
    issued_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket #{self.ticket_number}"
    
#don't use  
class Report(models.Model):
    report_type = models.CharField(max_length=50)  # e.g., Daily Sale
    generated_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.report_type} - {self.generated_at.date()}"

from django.db import models

#don't use
class SeatBooking(models.Model):
    busroute = models.ForeignKey(BusRoute, on_delete=models.CASCADE, blank=True,null=True)
    name = models.CharField(max_length=100)
    nrc = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    seat_number = models.CharField(max_length=5)
    fare = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.seat_number}"

class SeatBook(models.Model):
    
    route = models.ForeignKey(BusRoute, on_delete=models.CASCADE,blank=True, null=True)
    bus_number = models.ForeignKey(Bus, on_delete=models.CASCADE,blank=True, null=True)
    is_available = models.BooleanField(default=True)
    seat_number = models.ForeignKey(Seat, on_delete=models.CASCADE,blank=True, null=True)
    seat_status= models.PositiveIntegerField(default=1)
    name = models.CharField(max_length=100,blank=True, null=True)
    nrc = models.CharField(max_length=50,blank=True, null=True)
    phone = models.CharField(max_length=20,blank=True, null=True)
    amount = models.IntegerField(default=0)
    booked_date = models.DateField(auto_now_add=True, blank=True, null=True) 

    gender = models.CharField(max_length=10, blank=True, null=True)
    traveller_type = models.CharField(max_length=20, blank=True, null=True)
    special_request = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.seat_number} on {self.bus_number}"
    


