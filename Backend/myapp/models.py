# Backend/myapp/models.py
from django.db import models
from django.db.models import Q


class Vehicle(models.Model):
    FUEL_OPTIONS = [('Petrol','Petrol'),('Diesel','Diesel'),('Electric','Electric')]
    TRANSMISSION_OPTIONS = [('Manual','Manual'),('Automatic','Automatic'),('Semi Automatic','Semi Automatic')]
    STATUS_OPTIONS = [('Available','Available'),('Sold','Sold')]

    brand        = models.CharField(max_length=200)   # GIN trgm index added via migration
    model        = models.CharField(max_length=200)   # GIN trgm index added via migration
    year         = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    kilometers   = models.IntegerField(null=True, blank=True)
    fuel         = models.CharField(max_length=10, choices=FUEL_OPTIONS, blank=True)
    transmission = models.CharField(max_length=30, choices=TRANSMISSION_OPTIONS, blank=True)
    status       = models.CharField(max_length=10, choices=STATUS_OPTIONS, default='Available', blank=True)
    description  = models.TextField(blank=True)
    image        = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    is_featured  = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"

    class Meta:
        ordering = ['-id']
        indexes = [
            models.Index(fields=['brand']),
            models.Index(fields=['fuel']),
            models.Index(fields=['status']),
            models.Index(fields=['price']),
            models.Index(fields=['is_featured']),
            models.Index(
                fields=['status'],
                name='available_only_idx',
                condition=Q(status='Available'),
            ),
            # Composite index for common filter combos
            models.Index(fields=['status', 'is_featured'], name='status_featured_idx'),
            models.Index(fields=['status', 'fuel'],         name='status_fuel_idx'),
            models.Index(fields=['status', 'transmission'], name='status_transmission_idx'),
        ]


class VehicleImage(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='images')
    image   = models.ImageField(upload_to='vehicles/')

    def __str__(self):
        return f"Image for {self.vehicle.model}"
