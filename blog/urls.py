from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.AllBlogsView.as_view(), name='all_blogs'),
    path('blog/<int:author_pk>/', views.Blog.as_view(), name='user_blog'),
    path('blog/add-article/', views.CreateArticleView.as_view(), name='add_article'),
    path('blog/article/<int:pk>/', views.ArticleDetail.as_view(), name='article_detail'),
    path('blog/feed/', views.Feed.as_view(), name='feed'),
]
