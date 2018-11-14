from django.urls import path, include

from core import views
"""
admin_project_patterns = [
    path('', views.ProjectList.as_view(), name='admin_project_list'),
    path('create/', views.ProjectCreate.as_view(), name='admin_project_create'),
    path('view/(?P<pk>\d+)', views.ProjectView.as_view(), name='admin_project_view'),
    path('update/(?P<pk>\d+)', views.ProjectUpdate.as_view(), name='admin_project_update'),
]

admin_role_patterns = [
    path('', views.RoleList.as_view(), name='admin_role_list'),
    path('create/', views.RoleCreate.as_view(), name='admin_role_create'),
    path('view/(?P<pk>\d+)', views.RoleView.as_view(), name='admin_role_view'),
]
"""

admin_user_patterns = [
    path('', views.UserList.as_view(), name='admin_user_list'),
    path( 'create/', views.UserCreate.as_view(), name='admin_user_create'),
    #path('view/(?P<pk>\d+)', views.UserView.as_view(), name='admin_user_view'),
    #path('update/(?P<pk>\d+)', views.UserUpdate.as_view(), name='admin_user_update'),
]

urlpatterns = [
    path('admin/users/', include(admin_user_patterns)),
]

