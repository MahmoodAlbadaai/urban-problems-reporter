from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Basic pages
    path('', views.index, name='index'),
    path('report/', views.report, name='report'),
    path('map/', views.map, name='map'),
    path('success/', views.success, name='success'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('authority-dashboard/', views.authority_dashboard, name='authority_dashboard'),
    path('report/confirmation/', views.report_confirmation, name='report_confirmation'),
    
    # CRUD operations for issues
    path('issue/<int:pk>/', views.issue_detail, name='issue_detail'),
    path('issue/<int:pk>/update/', views.issue_update, name='issue_update'),
    path('issue/<int:pk>/delete/', views.issue_delete, name='issue_delete'),
    
    # Resolution operations
    path('issue/<int:pk>/resolve/', views.add_resolution, name='add_resolution'),
    path('issue/<int:pk>/resolution/update/', views.update_resolution, name='update_resolution'),
    
    # AJAX endpoints
    path('ajax/add-location/', views.ajax_add_location, name='ajax_add_location'),
    path('ajax/issue/<int:pk>/comment/', views.ajax_add_comment, name='ajax_add_comment'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)