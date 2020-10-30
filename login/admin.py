from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from login.forms import CustomUserChangeForm, CustomUserCreationForm
from login.models import User, Standard, Subject

#custom user admin 
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('name', 'email', 'class_no', 'subject', 'is_staff', 'is_student')
    list_filter = ('class_no',  'subject', 'is_staff', 'is_student')
    fieldsets = (
        (None, {'fields':('email', 'password', 'class_no', 'location', 'mobile_no', 'is_student')}),
         ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_student')}
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