from django.urls import path
from . import views
from django.views.generic import TemplateView, RedirectView


app_name = 'blog'

urlpatterns = [
    path('fbv-index/', views.indexView, name='fbv-index'),
    # path('cbv-index/', TemplateView.as_view(template_name='index.html', extra_context={'name': 'Amir'}))
    path('cbv-index/', views.IndexView.as_view(), name='cbv-index'),
    path('go-to-django/<int:pk>/', views.RedirectToDjango.as_view(), name='go-to-django'),
    
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    
    path('post/create/', views.PostCreateView.as_view()),
    path('post/<int:pk>/edit/', views.PostEditView.as_view(), name='post-edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
]
