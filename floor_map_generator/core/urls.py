from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('generate/', views.generate, name='generate'),
    path('floor-map/<int:floor_map_id>/', views.view_floor_map, name='view_floor_map'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('generate-map/', csrf_exempt(views.generate_map), name='generate_map'),
]