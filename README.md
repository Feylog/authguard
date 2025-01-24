AuthGuard – Микросервис для аутентификации и авторизации

AuthGuard – это микросервис, написанный на FastAPI, который обеспечивает: 1. Регистрацию пользователей (/auth/register). 2. Авторизацию с выдачей JWT-токена (/auth/login). 3. Поддержку защищенных маршрутов, доступных только авторизованным пользователям. 4. Возможность мониторинга метрик через Prometheus и Grafana.

Особенности
• FastAPI как базовый фреймворк.
• PostgreSQL для хранения пользователей и связанной информации.
• SQLAlchemy для работы с базой данных.
• Prometheus-FastAPI-Instrumentator для предоставления метрик на /metrics.
• Docker и Kubernetes для контейнеризации и оркестрации.

Структура проекта

authguard/
├── app/
│ ├── main.py # Точка входа приложения (FastAPI)
│ ├── database.py # Подключение к БД, создание таблиц, синтетические данные
│ ├── models/ # SQLAlchemy модели (User и т.д.)
│ ├── routes/ # Маршруты (auth.py, protected.py)
│ ├── services/ # Сервисы (логика аутентификации, генерации токена)
│ └── ...
├── Dockerfile # Инструкция для сборки Docker-образа
├── requirements.txt # Зависимости Python
├── k8s/ # Манифесты Kubernetes
│ ├── namespace.yaml # Namespace authguard
│ ├── postgres-deployment.yaml
│ ├── postgres-service.yaml
│ ├── app-deployment.yaml
│ ├── app-service.yaml
│ ├── secret.yaml # Секреты (пароль к БД и т. п.)
│ └── configmap.yaml # ConfigMap для не секретных переменных
└── README.md

Запуск приложения локально (без Kubernetes) 1. Установка зависимостей:

pip install -r requirements.txt

    2.	Запуск:

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

    3.	Откройте в браузере: http://localhost:8000

Контейнеризация 1. Собрать Docker-образ:

docker build -t <your-dockerhub-user>/authguard:latest .

    2.	Запустить контейнер:

docker run -p 8000:8000 <your-dockerhub-user>/authguard:latest

    3.	Перейдите на http://localhost:8000

Развертывание в Kubernetes

1. Подготовка

Убедитесь, что у вас есть кластер Kubernetes (например, Minikube) и kubectl настроен правильно:

minikube start # или kubectl config use-context ...

2. Применение манифестов

kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/postgres-deployment.yaml -n authguard
kubectl apply -f k8s/postgres-service.yaml -n authguard
kubectl apply -f k8s/secret.yaml -n authguard
kubectl apply -f k8s/configmap.yaml -n authguard
kubectl apply -f k8s/app-deployment.yaml -n authguard
kubectl apply -f k8s/app-service.yaml -n authguard

3. Проверка

kubectl get pods -n authguard
kubectl get svc -n authguard

    •	Pod authguard и postgres должны быть в статусе Running.
    •	Service authguard-svc будет доступен либо через NodePort, либо через minikube service authguard-svc -n authguard.

Мониторинг с Prometheus и Grafana

1. Настройка метрик в приложении

В main.py добавлен prometheus-fastapi-instrumentator, чтобы эндпоинт /metrics отдавал метрики Prometheus.
Проверить можно:

# Прямо в кластере:

kubectl port-forward svc/authguard-svc 8000:8000 -n authguard
curl http://localhost:8000/metrics

2. Установка Prometheus и Grafana (через Helm)

# Установка Prometheus

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/prometheus --namespace monitoring --create-namespace

# Установка Grafana

helm repo add grafana https://grafana.github.io/helm-charts
helm install grafana grafana/grafana --namespace monitoring

3. Настройка Prometheus-сервер

Добавьте блок в scrape_configs, чтобы Prometheus собирал метрики:

- job_name: 'authguard'
  metrics_path: /metrics
  static_configs:
  - targets: ['authguard-svc.authguard.svc.cluster.local:8000']

4. Подключение Grafana
   1. Зайдите в Grafana (NodePort или helm port-forward ...).
   2. Логин (по умолчанию admin / пароль в kubectl get secret grafana -n monitoring).
   3. Добавьте источник данных Prometheus, указав URL http://prometheus-server:80.
   4. Создайте Dashboard и выберите метрики приложения (например, http_request_duration_seconds_count).

Частые проблемы 1. Pod CrashLoopBackOff – проверьте логи (kubectl logs) и правильность переменных окружения (DATABASE_URL, секреты). 2. “Method Not Allowed” – убедитесь, что используете корректный метод (POST /auth/login). 3. 404 на /metrics – нужно, чтобы Instrumentator был корректно установлен и вызван в вашем main.py (до старта приложения, или через асинхронный startup_event).

Запуск в Replit

Если хотите использовать Replit: 1. Добавьте файл .replit и replit.nix (зависящие от того, как Replit обрабатывает Python). 2. Укажите команду запуска, например:

uvicorn app.main:app --host 0.0.0.0 --port 8000

    3.	Проверьте, что порты, используемые Replit, совпадают.

Лицензия

Добавьте раздел лицензии, если используется MIT или другая:

© 2025 Feylog. This project is licensed under the MIT License - see the LICENSE.md file for details.

Авторы и контакты
• Feylog – Инициатор проекта, Telegram: @feylog
• Pull Requests и Issues приветствуются!

Спасибо за использование AuthGuard! Если возникли проблемы – открывайте Issue или пишите в Pull Request. Удачи в разработке!
