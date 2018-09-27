from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('<int:author_pk>/', views.Blog.as_view(), name='user_blog'),
    path('add-article/', views.CreateArticleView.as_view(), name='add_article'),
    path('feed/', views.Feed.as_view(), name='feed'),
]
