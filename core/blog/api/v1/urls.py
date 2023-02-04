from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from . import views


app_name = 'api-v1'

router = SimpleRouter()
router.register('posts', views.PostViewSet, basename='post')
router.register('categories', views.CategoryModelViewSet, basename='category')

urlpatterns = [
    # path('post/', views.post_list, name='post-list'),
    # path('post/', views.PostList.as_view(), name='post-list'),
    # path('post/<int:pk>/', views.post_detail, name='post-detail'),
    # path('post/<int:pk>/', views.PostDetail.as_view(), name='post-detail'),
    # path('post/', views.PostViewSet.as_view({'get': 'list'}), name='post-list'),
    # path('post/<int:pk>/', views.PostViewSet.as_view({'get': 'retrieve'}), name='post-detail'),
]
urlpatterns += router.urls
