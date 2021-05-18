from django.urls import path
from . import views

urlpatterns = [
    path('update/', views.UpdateUserView.as_view(), name='update-user'),
    path('me/', views.UserProfileView.as_view(), name='me'),
    path('exists/', views.UserExistView.as_view(), name='user-exists'),
    path('roles/', views.ListUserRolesView.as_view(), name='user-roles'),
    path('settings/', views.UserSettingView.as_view(), name='user-setting-receive-notify'),
    path('settings/<uuid:pk>/', views.UserSettingDetailView.as_view(),
         name='user-setting-receive-notify-detail-detail-update')
]
