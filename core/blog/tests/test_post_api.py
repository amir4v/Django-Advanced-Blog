from django.contrib.auth import get_user_model
import pytest
from blog.models import Post
from rest_framework.test import APIClient
from django.urls import reverse
from datetime import datetime


User = get_user_model()


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def user():
    user = User.objects.create_user(email='user@example.com', password='password233@#@@#')
    return user


@pytest.fixture
def profile():
    user = User.objects.create_user(email='user2@example.com', password='password2-233@#@@#')
    return user.profile_set.all()[0]


@pytest.mark.django_db
class TestPostAPI:
    def test_get_post_response_200_status(self, api_client):
        url = reverse('blog:api-v1:post-list')
        response = api_client.get(url)
        assert response.status_code == 200
    
    def test_create_post_response_401_status(self, api_client):
        url = reverse('blog:api-v1:post-list')
        response = api_client.post(url, data={
            'title': 'sssss',
            'content': 'ssssss',
            'status': True,
            'published_dt': datetime.now(),
        })
        assert response.status_code == 401
    
    def test_create_post_response_201_status(self, api_client, user):
        url = reverse('blog:api-v1:post-list')
        # api_client.force_login(user)
        api_client.force_authenticate(user)
        response = api_client.post(url, data={
            'title': 'sssss',
            'content': 'ssssss',
            'status': True,
            'published_dt': datetime.now(),
        })
        assert response.status_code == 201
    
    def test_create_post_invalid_data_response_400_status(self, api_client, user):
        url = reverse('blog:api-v1:post-list')
        api_client.force_login(user)
        response = api_client.post(url, data={
            'title': 'sssss',
            'content': 'ssssss',
        })
        assert response.status_code == 400
