from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

CustomUser = get_user_model()

class CustomUserAdmin(UserAdmin):
    
    model = CustomUser
    list_display = ('email', 'is_staff')
    ordering = ('email',)
    
    add_fieldsets = (
        (None, {"fields": ("email", "password", )}),
        (_("Personal info"), {"fields": ( )}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    


admin.site.register(CustomUser, CustomUserAdmin)
 