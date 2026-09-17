from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FeeStructureViewSet,
    StudentFeeViewSet,
    PaymentRecordViewSet,
    fee_dashboard_view
)

app_name = 'fees'

router = DefaultRouter()
router.register(r'structures', FeeStructureViewSet, basename='fee-structure')
router.register(r'student-fees', StudentFeeViewSet, basename='student-fee')
router.register(r'payments', PaymentRecordViewSet, basename='payment-record')

urlpatterns = [
    # Web Routes
    path('', fee_dashboard_view, name='fee_dashboard'),

    # API Routes
    path('api/', include(router.urls)),
]
