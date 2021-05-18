from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register
)

from .models import UserRole


class UserRoleAdmin(ModelAdmin):
    model = UserRole
    menu_label = 'UserRole'
    menu_icon = 'fa-folder-open'
    add_to_settings_menu = True
    list_display = ('name', 'role', 'description')
    list_filter = ('role',)
    ordering = ('name',)


modeladmin_register(UserRoleAdmin)