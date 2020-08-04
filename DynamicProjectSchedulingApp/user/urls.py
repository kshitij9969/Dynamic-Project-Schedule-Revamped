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
    path('me_org/', views.ManageOrganisationAccountView.as_view(), name='me-org'),
    path('create_manager/', views.CreateManagerAccountView.as_view(), name='create-manager'),
    path('me_manager/', views.ManageManagerAccountView.as_view(), name='me-manager'),
    path('create_associate/', views.CreateAssociateAccountView.as_view(), name='create-associate'),
    path('me_associate/', views.ManageAssociateAccountView.as_view(), name='me-associate'),
]
