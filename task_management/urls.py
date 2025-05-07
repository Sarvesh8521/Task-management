from django.urls import path, include
from tasks.tasksviews import task_views, project_views, organisation_views
from user_details.userviews import user_views, profile_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('users/', include([
        path('create/', user_views.create_user, name='create_user'),
        path('update/<int:user_id>/', user_views.update_user, name='update_user'),
        path('search/<int:user_id>', user_views.get_user, name='get_user'),
        # path('search/', user_views.search_users, name='search_user'),
        path('delete/<int:user_id>/', user_views.delete_user, name='delete_user'),  
    ])),

    
   
    path('profiles/details/<int:user_id>/', profile_views.get_profile, name='get_profile'),
    path('profiles/update/<int:user_id>/', profile_views.update_profile, name='update_profile'),
    path('profiles/create/', profile_views.create_profile, name='create_profile'),
    path('profiles/delete/<int:user_id>/', profile_views.delete_profile, name='delete_profile'),

    
    path('organizations/', include([
        path('create/', organisation_views.create_organization, name='create_organization'),
        path('update/<int:org_id>/', organisation_views.update_organization, name='update_organization'),
        path('search/<int:org_id>', organisation_views.get_organization, name='get_organization'),
        path('delete/<int:org_id>/', organisation_views.delete_organization, name='delete_organization'), 
        # path('all/', organisation_views.get_organizations, name='get_organizations'),  
        path('get/<int:org_id>/', organisation_views.get_organization, name='get_organization'),
    ])),


    #path('projects/', include(project_views.urlpatterns)),
    path('projects/create/', project_views.create_project, name='create_project'),
    path('projects/update/<int:project_id>/', project_views.update_project, name='update_project'),
    path('projects/delete/<int:project_id>/', project_views.delete_project, name='delete_project'),
    # path('projects/search/', project_views.search_projects, name='search_projects'),
    path('projects/all/', project_views.get_all_projects, name='get_all_projects'),


    
    path('tasks/', include(
        [path('create/', task_views.create_task, name='create_task'),
        path('update/<int:task_id>/', task_views.update_task, name='update_task'),
        path('assign/<int:task_id>/<int:user_id>/', task_views.assign_task, name='assign_task'),
        path('all/', task_views.get_tasks, name='get_tasks'),
        # path('get/<int:task_id>/', task_views.get_task, name='get_task'),
        path('all/', task_views.get_tasks, name='get_tasks'),
        path('search/', task_views.search_tasks, name='search_tasks'),
        path('delete/<int:task_id>/', task_views.delete_task, name='delete_task'),
    ])),

]
