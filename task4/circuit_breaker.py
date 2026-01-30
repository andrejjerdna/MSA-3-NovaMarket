from locust import HttpUser, task, between, events
import json

class LogisticsUser(HttpUser):
    wait_time = between(0.3, 1.5)
    
    # Быстрые успешные запросы (основная нагрузка)
    @task(10)
    def fast_endpoint(self):
        self._check_endpoint("/logistics", expected_status=200)

    
    def _check_endpoint(self, path, expected_status=None, name=None, timeout=5.0):
        with self.client.get(
            path,
            catch_response=True,
            name=name or path,
            timeout=timeout
        ) as response:
            try:
                data = response.json()
                # Валидация структуры ответа
                if "status" not in data:
                    response.failure("Missing 'status' field in JSON")
                    return
                
                # Проверка ожидаемого статуса ответа
                if expected_status and response.status_code != expected_status:
                    response.failure(
                        f"Status mismatch: expected {expected_status}, got {response.status_code}. "
                        f"Response: {data.get('message', 'N/A')}"
                    )
                    return
          
                response.success()
            
            except json.JSONDecodeError:
                if response.text.strip():  # Не пустой ответ без JSON
                    response.failure(f"Invalid JSON: {response.text[:100]}")
                else:
                    response.failure("Empty response")
            except Exception as e:
                response.failure(f"Validation error: {str(e)}")
