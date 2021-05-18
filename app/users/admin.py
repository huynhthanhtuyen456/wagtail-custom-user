# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
# from django.utils.translation import ugettext_lazy as _
#
# from .forms import CustomUserChangeForm, CustomUserCreationForm
# from .models import User, ConfirmCode, UserRole, UserSetting
#
#
# class UserAdmin(AuthUserAdmin):
#     form = CustomUserChangeForm
#     add_form = CustomUserCreationForm
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         (_('Personal info'), {'fields': ('first_name',
#                                          'last_name',)}),
#         (_('Permissions'), {'fields': ('role',
#                                        'is_active',
#                                        'is_staff',
#                                        'is_superuser',
#                                        'groups',
#                                        'user_permissions')}),
#         (_('Important dates'), {'fields': ('last_login',)}),
#         (_('Document'), {'fields': ('avatar_url',
#                                     'proof_of_identification_url',
#                                     'profile_video_url',
#                                     'youtube_url')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password1', 'password2'),
#         }),
#     )
#     list_display = ('user_id', 'email', 'first_name', 'last_name', 'is_active')
#     search_fields = ('email', 'first_name', 'last_name')
#     ordering = ('email',)
#
#     def get_queryset(self, request):
#         return super(UserAdmin, self).get_queryset(request)
#
#     def has_add_permission(self, request):
#         return True
#
#
# admin.site.register(User, UserAdmin)
#
# admin.site.register(UserRole)
#
#
# @admin.register(ConfirmCode)
# class ConfirmCode(admin.ModelAdmin):
#     list_display = ('id', 'code', 'email', 'expire_date')
#
#
# @admin.register(UserSetting)
# class UserSettingAdmin(admin.ModelAdmin):
#     list_display = ('uuid', 'user', 'role', 'notice_mail', 'notice_sms', 'notice_fire_base')
