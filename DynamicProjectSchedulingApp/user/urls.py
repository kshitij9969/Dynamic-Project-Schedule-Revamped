from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    # path('create/', views.CreateUserView.as_view(), name='create'),
    path('login/', views.LoginView.as_view(), name='token'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('homepage/', views.HomePageView.as_view(), name='homepage'),
    # path('me/', views.ManageUserView.as_view(), name='me'),
    path('create_org/', views.CreateOrganisationAccountView.as_view(), name='create-org'),
    path('me_org/', views.UpdateOrganisationAccountView.as_view(), name='update-org'),
    path('create_manager/', views.CreateManagerAccountView.as_view(), name='create-manager'),
    path('me_manager/', views.UpdateManagerAccountView.as_view(), name='update-manager'),
    path('create_associate/', views.CreateAssociateAccountView.as_view(), name='create-associate'),
    path('me_associate/', views.UpdateAssociateAccountView.as_view(), name='update-associate'),
    path('get_associate_list/', views.GetAssociateListApi.as_view(), name='get-associate-list'),
    path('get_manager_list/', views.GetManagerListApi.as_view(), name='get-manager-list'),
    path('delete_organisation/', views.DeleteOrganisationViewApi.as_view(), name='delete-org'),
    path('delete_manager/', views.DeleteManagerViewApi.as_view(), name='delete-manager'),
    path('delete_associate/', views.DeleteAssociateViewApi.as_view(), name='delete-associate'),
    path('get_my_profile/', views.GetMyProfileApi.as_view(), name='get-my-profile'),
    path('change_password/', views.ResetPasswordApi.as_view(), name='change-password')
]
