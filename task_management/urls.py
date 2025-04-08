from django.urls import path, include
from tasks.tasksviews import task_views, project_views, organisation_views
from user_details.userviews import user_views, profile_views

urlpatterns = [
    
    path('users/', include([
        path('create/', user_views.create_user, name='create_user'),
        path('update/<int:user_id>/', user_views.update_user, name='update_user'),
        path('search/', user_views.get_user, name='get_user'),  
    ])),

    
   
    path('profiles/details/<int:user_id>/', profile_views.get_profile, name='get_profile'),
    path('profiles/update/<int:user_id>/', profile_views.update_profile, name='update_profile'),
    path('profiles/create/<int:user_id>/', profile_views.create_profile, name='create_profile'),

    
    path('organizations/', include([
        path('create/', organisation_views.create_organization, name='create_organization'),
        path('update/<int:org_id>/', organisation_views.update_organization, name='update_organization'),
    ])),


    #path('projects/', include(project_views.urlpatterns)),
    path('projects/create/', project_views.create_project, name='create_project'),
    path('projects/update/<int:project_id>/', project_views.update_project, name='update_project'),


    
    path('tasks/', include([
        path('create/', task_views.create_task, name='create_task'),
        path('update/<int:task_id>/', task_views.update_task, name='update_task'),
        path('assign/<int:task_id>/<int:user_id>/', task_views.assign_task, name='assign_task'),
        path('all/', task_views.get_tasks, name='get_tasks'),
        path('search/', task_views.search_tasks, name='search_tasks'),
    ])),
]
