# Backend/myapp/views.py
from rest_framework import generics, filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.db.models import Q, Case, When, Value, BooleanField
from .models import Vehicle, VehicleImage
from .serializers import VehicleSerializer
from .search_backends import FuzzySearchBackend   # ← NEW


# ── PUBLIC ───────────────────────────────────────────────────────────────────

class VehicleListAPIView(generics.ListAPIView):
    """Cars page — fuzzy search + filters + ordering"""
    serializer_class = VehicleSerializer
    authentication_classes = []
    permission_classes = [AllowAny]
    filter_backends = [
        DjangoFilterBackend,
        FuzzySearchBackend,          # ← replaces filters.SearchFilter
        filters.OrderingFilter,
    ]
    filterset_fields = ['brand', 'fuel', 'transmission', 'status']
    ordering_fields  = ['year', 'kilometers']
    # Featured first, then vehicles with a photo, then the rest; newest first within each group.
    ordering         = ['-is_featured', '-has_photo', '-id']

    def get_queryset(self):
        qs = Vehicle.objects.prefetch_related('images').annotate(
            has_photo=Case(
                When(Q(image__isnull=True) | Q(image=''), then=Value(False)),
                default=Value(True),
                output_field=BooleanField(),
            )
        )
        status = self.request.query_params.get('status')
        if status:
            return qs.filter(status=status)
        return qs.filter(status='Available')


class VehicleDetailAPIView(generics.RetrieveAPIView):
    serializer_class = VehicleSerializer
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = Vehicle.objects.all().prefetch_related('images')


class FeaturedVehicleListView(generics.ListAPIView):
    serializer_class = VehicleSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            Vehicle.objects
            .filter(is_featured=True, status='Available')
            .prefetch_related('images')
            .order_by('-id')
        )


# ── ADMIN ────────────────────────────────────────────────────────────────────

class VehicleAdminViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleSerializer
    permission_classes = [IsAdminUser]
    queryset = Vehicle.objects.all().prefetch_related('images').order_by('-id')
    filter_backends = [
        DjangoFilterBackend,
        FuzzySearchBackend,          # ← fuzzy search in admin too
        filters.OrderingFilter,
    ]
    filterset_fields  = ['brand', 'fuel', 'transmission', 'status', 'is_featured']
    ordering_fields   = ['year', 'kilometers', 'id']

    def perform_create(self, serializer):
        vehicle = serializer.save()
        for img in self.request.FILES.getlist('gallery_images'):
            VehicleImage.objects.create(vehicle=vehicle, image=img)

    def perform_update(self, serializer):
        vehicle = serializer.save()
        for img in self.request.FILES.getlist('gallery_images'):
            VehicleImage.objects.create(vehicle=vehicle, image=img)

    @action(detail=True, methods=['delete'], url_path='images/(?P<image_id>[^/.]+)')
    def delete_image(self, request, pk=None, image_id=None):
        try:
            img = VehicleImage.objects.get(id=image_id, vehicle_id=pk)
            img.image.delete(save=False)
            img.delete()
            return Response({'deleted': image_id})
        except VehicleImage.DoesNotExist:
            return Response({'error': 'Image not found'}, status=404)

    @action(detail=True, methods=['patch'], url_path='toggle-featured')
    def toggle_featured(self, request, pk=None):
        vehicle = self.get_object()
        vehicle.is_featured = not vehicle.is_featured
        vehicle.save(update_fields=['is_featured'])
        return Response({
            'id': vehicle.id,
            'is_featured': vehicle.is_featured,
            'message': f"{'⭐ Added to' if vehicle.is_featured else '✖ Removed from'} featured",
        })

    @action(detail=True, methods=['patch'], url_path='toggle-status')
    def toggle_status(self, request, pk=None):
        vehicle = self.get_object()
        vehicle.status = 'Sold' if vehicle.status == 'Available' else 'Available'
        vehicle.save(update_fields=['status'])
        return Response({'id': vehicle.id, 'status': vehicle.status})


class DashboardStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({
            'total_vehicles': Vehicle.objects.count(),
            'available':      Vehicle.objects.filter(status='Available').count(),
            'sold':           Vehicle.objects.filter(status='Sold').count(),
            'featured':       Vehicle.objects.filter(is_featured=True).count(),
        })