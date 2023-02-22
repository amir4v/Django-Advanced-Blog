from locust import HttpUser, task


class LB(HttpUser):
    def on_start(self):
        json_response = self.client.post('/accounts/api/v2/jwt/create/', data={'email': 'admin@admin.com', 'password': 'a/@12345678'}).json()
        self.client.headers = {'Authorization': f"Bearer {json_response.get('access')}"}
    
    @task
    def post_list(self):
        self.client.get('/blog/api/v1/post/')
    
    @task
    def category_list(self):
        self.client.get('/blog/api/v1/category/')
