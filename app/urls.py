from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from app import views


urlpatterns = ([
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('question/<int:question_id>', views.question, name='question'),
    path('ask/', views.ask, name='ask'),
    path('login/', views.Login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.Logout, name='logout'),
    path('settings/', views.settings, name='settings'),
    path('tag/<str:tag_name>', views.tag, name='tag'),
    path('question/<question_id>/like_async', views.like_async, name="like_async"),
    path('question/<answer_id>/like_async_answer', views.like_async_answer, name="like_async_answer"),
    path('question/<answer_id>/correct_async', views.correct_async, name="correct_async"),
    path('<question_id>/like_async', views.like_async, name="like_async"),
    path('tag/<question_id>/like_async', views.like_async, name="like_async"),
    path('hot/<question_id>/like_async', views.like_async, name="like_async"),
])

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
