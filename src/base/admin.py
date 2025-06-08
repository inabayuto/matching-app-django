from django.contrib import admin
from .models import User, Profile, Matching, DM
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    ordering = ('id',)
    list_display = ('email', 'password')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Information', {'fields': ('username',)}),
        (
            'Permissions',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
           'classes': ('wide',),
           'fields': ('email', 'password1', 'password2'),
        }),
    )
    inlines = (ProfileInline,)

class ProfileAdmin(admin.ModelAdmin):
    ordering = ('-created_at',)
    list_display = ('__str__', 'user', 'age', 'sex','created_at')

class MatchingAdmin(admin.ModelAdmin):
    ordering = ('-created_at',)
    list_display = ('__str__', 'approved', 'created_at')

class DMAdmin(admin.ModelAdmin):
    ordering = ('-created_at',)
    list_display = ('__str__', 'sender', 'receiver', 'created_at')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Matching, MatchingAdmin)
admin.site.register(DM, DMAdmin)

