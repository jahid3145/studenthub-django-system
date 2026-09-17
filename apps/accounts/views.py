from rest_framework import generics, viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import User
from .serializers import (
    CustomTokenObtainPairSerializer,
    UserSerializer,
    UserRegistrationSerializer,
    ChangePasswordSerializer
)
from .permissions import IsSuperAdmin, IsAdminOrStaff

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    """JWT Token Login API Endpoint."""
    serializer_class = CustomTokenObtainPairSerializer


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    """API endpoint to view and update the current user's profile."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordAPIView(APIView):
    """API endpoint to change user password."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response(
                {"success": True, "message": "Password updated successfully."},
                status=status.HTTP_200_OK
            )
        return Response(
            {"success": False, "message": "Password change failed.", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class UserViewSet(viewsets.ModelViewSet):
    """API ViewSet for User administration (Admins only)."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrStaff]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    filterset_fields = ['role', 'is_active']


# Web Views for Server-Side Rendered Interface
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('dashboard:index')
            else:
                messages.error(request, "Your account has been deactivated. Please contact administration.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('accounts:login')


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})
