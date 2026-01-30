import random
from locust import HttpUser, task, between

class ApiUser(HttpUser):
    wait_time = between(0.5, 2.0)
    
    @task(5)
    def web_request(self):
        """Запрос от веб-клиента"""
        self.client.get(
            "/api/user/profile",
            headers={"Client-Type": "web"},
            name="API_Web"
        )
    
    @task(3)
    def mobile_request(self):
        """Запрос от мобильного клиента"""
        self.client.get(
            "/api/order/status",
            headers={"Client-Type": "mobile"},
            name="API_Mobile"
        )
    
    def on_start(self):
        """Выполняется при старте пользователя"""
        self.client.verify = False  # Отключаем проверку SSL (для локальных тестов)