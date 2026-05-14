from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register_user, name="register"),
    path('store/', views.shopping, name="store"),
    path('product/<int:pk>', views.product, name="product"),
    path('category_detail/<str:slug>', views.category_detail, name='category_detail'),
    path('search/', views.search, name="search"),
    # Profile URLs
    path('profile/', views.profile_view, name="profile"),
    path('profile/edit/', views.edit_profile, name="edit_profile"),
    path('profile/change-password/', views.change_password, name="change_password"),
    path('profile/upload-picture/', views.upload_profile_picture, name="upload_profile_picture"),
    path('profile/delete-picture/', views.delete_profile_picture, name="delete_profile_picture"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
