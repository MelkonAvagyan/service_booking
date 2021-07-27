from django.urls import path
import register.views as rv
import users.views as uv
import main.views as mv
   

app_name = 'registration'

urlpatterns = [
    path('', mv.HomePageView.as_view(),name='home'),
    path('client_registration/', rv.ClientRegistration.as_view(), name='client_registration'),
    path('specialist_registration/', rv.SpecialistRegistration.as_view(), name='specialist_registration'),
    path('login/', rv.LoginView.as_view(), name='login'),
    path('logout/', rv.LogOutView.as_view(), name='logout'),
    path('account/<slug:specialist_account_slug>/', uv.SpecialistProfile.as_view(), name='specialist_account'),
    path('account/<slug:client_account_slug>/', uv.ClientProfile.as_view(), name='client_account'),
]
