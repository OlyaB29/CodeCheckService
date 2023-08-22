from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, File, Log
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'user', 'is_new')
    list_filter = ('is_new', 'created_at', 'updated_at', 'user')


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'report', 'is_send_notice')
    list_filter = ('file', 'date', 'is_send_notice')
