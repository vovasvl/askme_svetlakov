from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from app import views


urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('question/<int:question_id>', views.question, name='question'),
    path('ask/', views.ask, name='ask'),
    path('login/', views.Login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.Logout, name='logout'),
    path('settings/', views.settings, name='settings'),
    path('tag/<str:tag_name>', views.tag, name='tag'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
