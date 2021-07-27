from django.urls import path
import main.views as mv
import register.views as rv
import users.views as uv
   
app_name = 'phoenix'
urlpatterns = [
    path('', mv.HomePageView.as_view(),name='home'),
    path('about/', mv.AboutPageView.as_view(),name='about'),
    # path('contact/',),
    # path('careers/'),
    # path('blog/',)
]