from django.urls import path
import users.views as uv
import register.views as rv
import main.views as mv
   
app_name = 'accounts'
urlpatterns = [
    path('client/<int:pk>/', uv.Clients.as_view(), name='client'),
    
    path('Self-Beauty-Care',uv.SpecialistsList.as_view(), name='care'),
    path('Education',uv.SpecialistsList.as_view(), name='education'),
    path('Software-Services',uv.SpecialistsList.as_view(), name='software'),
    path('Home-Services',uv.SpecialistsList.as_view(), name='home'),
    path('Handmade-Products',uv.SpecialistsList.as_view(), name='handmade'),
    path('reviews/', uv.Reviews.as_view(), name='reviews'),
    path('specialists/<int:pk>/', uv.SpecialistDetailView.as_view(), name='specialist_details'),
    #path('category/<str:pk>/', views.category),