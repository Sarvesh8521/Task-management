from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenRefreshView

from tasks.tasksviews import task_views, project_views, organisation_views
from user_details.userviews import user_views, profile_views
from task_management.auth_views import login_view


urlpatterns = [
    # Authentication
    path('api/auth/login/', login_view, name='login'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Users
    path('api/users/', include([
        path('create/', user_views.create_user, name='create_user'),
        path('update/<int:user_id>/', user_views.update_user, name='update_user'),
        path('<int:user_id>/', user_views.get_user, name='get_user'),
        path('delete/<int:user_id>/', user_views.delete_user, name='delete_user'),
        path('search/', user_views.search_users, name='search_users'),
    ])),

    # Profiles
    path('api/profiles/', include([
        path('create/', profile_views.create_profile, name='create_profile'),
        path('<int:user_id>/', profile_views.get_profile, name='get_profile'),
        path('update/<int:user_id>/', profile_views.update_profile, name='update_profile'),
        path('delete/<int:user_id>/', profile_views.delete_profile, name='delete_profile'),
    ])),

    # Organizations
    path('api/organizations/', include([
        path('create/', organisation_views.create_organization, name='create_organization'),
        path('update/<int:org_id>/', organisation_views.update_organization, name='update_organization'),
        path('<int:org_id>/', organisation_views.get_organization, name='get_organization'),
        path('delete/<int:org_id>/', organisation_views.delete_organization, name='delete_organization'),
    ])),

    # Projects
    path('api/projects/', include([
        path('create/', project_views.create_project, name='create_project'),
        path('update/<int:project_id>/', project_views.update_project, name='update_project'),
        path('delete/<int:project_id>/', project_views.delete_project, name='delete_project'),
        path('all/', project_views.get_all_projects, name='get_all_projects'),
    ])),

    # Tasks
    path('api/tasks/', include([
        path('create/', task_views.create_task, name='create_task'),
        path('update/<int:task_id>/', task_views.update_task, name='update_task'),
        path('assign/<int:task_id>/<int:user_id>/', task_views.assign_task, name='assign_task'),
        path('all/', task_views.get_tasks, name='get_tasks'),
        path('search/', task_views.search_tasks, name='search_tasks'),
        path('delete/<int:task_id>/', task_views.delete_task, name='delete_task'),
    ])),

    # Frontend - serve index.html for all non-API routes
    path('', TemplateView.as_view(template_name='index.html'), name='frontend'),
]
