from django.contrib import admin
from .models import TeacherProfile


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'get_full_name', 'department', 'designation', 'joining_date']
    search_fields = ['employee_id', 'user__first_name', 'user__last_name', 'user__email']
    list_filter = ['department', 'designation']

    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Teacher Name'
