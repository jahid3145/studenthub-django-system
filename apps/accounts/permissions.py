from rest_framework import permissions


class IsSuperAdmin(permissions.BasePermission):
    """Allows access only to Super Admin users."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superadmin)


class IsAdminOrStaff(permissions.BasePermission):
    """Allows access to Super Admin or Admin/Staff users."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_admin_or_staff)


class IsTeacher(permissions.BasePermission):
    """Allows access only to Teacher users."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_teacher)


class IsStudent(permissions.BasePermission):
    """Allows access only to Student users."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_student)


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission allowing users to access/modify only their own objects,
    unless they are an Admin/Staff member.
    """
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_admin_or_staff:
            return True
        
        # Check standard user relationships
        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'student') and hasattr(obj.student, 'user'):
            return obj.student.user == request.user
        if hasattr(obj, 'teacher') and hasattr(obj.teacher, 'user'):
            return obj.teacher.user == request.user
        
        return obj == request.user
