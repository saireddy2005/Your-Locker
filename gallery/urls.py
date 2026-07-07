from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('home/',views.home,name="home"),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path("home/", views.home, name="home"),
    path("upload/", views.upload_file, name="upload_file"),
    path("view/<int:file_id>/",views.view_file,name="view_file"),
    path("delete/<int:file_id>/", views.delete_file, name="delete_file"),
    path("logout/", views.logout_view, name="logout"),
path("edit-username/", views.edit_username, name="edit_username"),
path("change-password/",views.change_password,name="change_password"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)