from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from login.forms import CustomUserChangeForm, CustomUserCreationForm
from login.models import User, Standard, Subject


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'class_no', 'is_staff', 'is_active')
    list_filter = ('email','class_no',  'is_staff','is_active')
    fieldsets = (
        (None, {'fields':('email', 'password', 'class_no', 'location', 'mobile_no')}),
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


class SubjectA(admin.ModelAdmin):
    list_display = ("name", "class_no")
    list_filter = ("class_no",)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Standard)
admin.site.register(Subject, SubjectA)

#Admin site changes
admin.site.site_header = "Admin Page"