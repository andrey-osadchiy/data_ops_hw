
# __Задание 1: MLFlow__


В рамках первого задания был развернут локальный сервер **MLflow** с использованием **Docker Compose**.

MLflow используется для:
- отслеживания экспериментов машинного обучения
- логирования параметров и метрик
- хранения артефактов моделей
- ведения реестра моделей

В данной работе был реализован локальный deployment MLflow с использованием:
- **MLflow server**
- **PostgreSQL** как backend store
- **Docker Compose** для оркестрации сервисов

---

# Архитектура решения

Использую следующие компоненты:

- **MLflow server** — веб-интерфейс и API для работы с экспериментами
- **PostgreSQL** — хранение метаданных экспериментов
- **MinIO** — объектное хранилище для артефактов (если используется вариант 2)

Схема:

``` id="ezz54h"
Python script / Jupyter
        |
        v
   MLflow server
        |
        v
 PostgreSQL (metadata)
        |
        v
   MinIO (artifacts)
```

```bash
01-mlflow/
├── Dockerfile
├── docker-compose.yaml
├── .env
├── run_experiment.py
└── README.md
```
#### Dockerfile

В образ устанавливаются необходимые зависимости:
- mlflow
- psycopg2-binary
- gevent
- boto3

#### docker-compose.yaml
С помощью Docker Compose поднимаются сервисы:
- db — PostgreSQL
- mlflow — MLflow server
- minio — S3-compatible storage

#### Переменные окружения

В файле .env задаются:

__PostgreSQL__:
- POSTGRES_DB
- POSTGRES_USER
- POSTGRES_PASSWORD

__MLflow__:
- MLFLOW_SERVER_FILE_STORE

__MinIO__:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_BUCKET
- AWS_URL

### Запуск проекта

Сборка и запуск:
```bash
docker compose build
docker compose up -d
```

### Доступ к MLflow

После запуска интерфейс доступен по адресу:
```bash
http://localhost:8080
```
![Скриншот](docs/01-mlflow/1.png)
Создали эксперимент, важно убедиться, что MLflow создал таблицы.
![Скриншот](docs/01-mlflow/2.png)

Тестовый эксперимент

Для проверки работы MLflow был создан файл run_experiment.py

Содержимое файла:
```python
import mlflow

mlflow.set_tracking_uri("http://localhost:8080")
mlflow.set_experiment("mlflow-hw-experiment")

with mlflow.start_run():
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_param("batch_size", 32)
    mlflow.log_metric("accuracy", 0.95)
    mlflow.log_metric("loss", 0.12)

print("Experiment logged successfully")
```
Запуск:
```bash
python run_experiment.py
```
После выполнения в MLflow появился новый run с параметрами и метриками.
![Скриншот](docs/01-mlflow/3.png)


# __Задание 2: Airflow__

В рамках второго задания был развернут локальный кластер Apache Airflow с использованием Docker Compose.
Airflow используется для оркестрации и автоматизации пайплайнов обработки данных (ETL / ML pipelines).

В работе была реализована следующая архитектура:
- Apache Airflow Webserver — веб-интерфейс для управления DAG
- Apache Airflow Scheduler — планирование и запуск задач
- Apache Airflow Triggerer — обработка асинхронных триггеров
- PostgreSQL — backend database для хранения метаданных Airflow

Архитектура пайплайна:
```bash
            +------------------+
            |  Airflow UI      |
            |  (Webserver)     |
            +---------+--------+
                      |
                      v
            +------------------+
            |    Scheduler     |
            +---------+--------+
                      |
                      v
           +---------------------+
           |        DAG          |
           |                     |
           | extract_data       |
           | extract_clickhouse |
           |        ↓           |
           |        train       |
           +---------------------+

                      |
                      v
                PostgreSQL
           (Airflow metadata DB)
```

### Структура проекта
```bash
02-airflow
├── docker-compose.yaml
├── .env
└── data/
    └── airflow/
        └── dags/
            ├── __init__.py
            └── firstproj/
                ├── __init__.py
                ├── first_dag.py
                └── runner.py
```

### Переменные окружения

Файл .env содержит конфигурацию для Postgres и Airflow.

PostgreSQL
```bash
POSTGRES_PASSWORD=airflowdbpwd
```

Airflow database connection
```bash
AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql://airflow:airflowdbpwd@db:5432/airflow
```

Secret key
```bash
APP_SECRET_KEY=airflowsecretkey
```

### Запуск проекта

1. Запуск PostgreSQL
```bash
docker compose up -d db
```

2. Инициализация базы данных Airflow
```bash
docker compose up airflow.db.init
```

3. Применение миграций
```bash
docker compose up airflow.db.migrate
```

4. Запуск основных сервисов Airflow
```bash
docker compose up -d airflow.webserver
docker compose up -d airflow.scheduler
docker compose up -d airflow.triggerer
```

### Доступ к Airflow

После запуска веб-интерфейс доступен по адресу:
```bash
http://localhost:8080
```

#### Создание администратора

Для доступа к интерфейсу был создан пользователь admin.

Выполняется внутри контейнера:
```bash
docker compose exec -it airflow.webserver bash

airflow users create \
  --username admin \
  --firstname Andrey \
  --lastname Osad \
  --role Admin \
  --email admin@example.org
```


###  DAG

В проекте реализован DAG first => data/airflow/dags/firstproj/first_dag.py

конфигурация:
```python
dag = DAG(
    "first",
    schedule="33 4 * * *",
    start_date=datetime.fromisoformat("2026-02-10T10:10:10+00:00"),
    catchup=False,
)
```

Реализованные задачи

В DAG реализованы три задачи:

- extract_data (Имитация извлечения данных.)
- extract_from_clickhouse (Имитация загрузки данных из ClickHouse.)
- train (Имитация обучения модели.)

__Зависимости задач__
```bash
extract_data
extract_from_clickhouse
        ↓
       train
```
### Запуск DAG

DAG запускается вручную через интерфейс Airflow.

Шаги:
1. открыть DAGs
2. включить DAG first
3. нажать Trigger DAG
После запуска задачи выполняются последовательно.
![Скриншот](docs/02-airflow/1.png)
![Скриншот](docs/02-airflow/2.png)
Из скриншотов видно, вдаг отработал успшено.

Отлично, всё получилось!


# __Задание 3: LakeFS__

В рамках задания была поднята локальная инфраструктура:

- **PostgreSQL** — метаданные lakeFS
- **MinIO** — S3-совместимое объектное хранилище
- **lakeFS** — система версионирования данных
- **lakectl** — CLI для работы с lakeFS

```bash
docker compose up -d
```
Для начала поднимаем Postgres
![Скриншот](docs/03-lakefs/1.png)

Далее поднимаем Minio
![Скриншот](docs/03-lakefs/2.png)

Заходим в Minio
![Скриншот](docs/03-lakefs/3.png)

- MinIO Console -  http://localhost:9001
- MinIO S3 API - http://localhost:9000

Создаём бакет lakefs
![Скриншот](docs/03-lakefs/4.png)

Поднимаем Lakefs
![Скриншот](docs/03-lakefs/5.png)

При первом запуске был выполнен setup:
```bash
http://localhost:8000/setup
```
В процессе настройки были созданы:
	•	Access Key
	•	Secret Key
  
Вводим данные и получаем credidentials
![Скриншот](docs/03-lakefs/6.png)
![Скриншот](docs/03-lakefs/7.png)
![Скриншот](docs/03-lakefs/8.png)

Эти ключи использовались для настройки CLI

После создаём репозиторий
![Скриншот](docs/03-lakefs/9.png)
![Скриншот](docs/03-lakefs/10.png)

Была создана новая ветка
```bash
featone
```
Она используется как рабочая ветка для изменения данных.

![Скриншот](docs/03-lakefs/11.png)

В репозиторий был добавлен новый файл:
```bash
echo "hello lakefs" > firstrepo/data.txt
```

Изменения были зафиксированы в lakeFS:
![Скриншот](docs/03-lakefs12.png)

После compare main и featone был сделан merge
![Скриншот](docs/03-lakefs/13.png)

Итоговая структура репозитория

В ветке main находятся:
```bash
README.md
data.txt
data/
images/
lakes.parquet
```
![Скриншот](docs/03-lakefs/14.png)

Отлично, всё получилось!

# Задание 4 jupyterhub
В рамках 4 задания был локально развернут jupyterhub сервер, были запущены в нем инстансы jupyterlab и проведены там исследования

### Структура проекта

```bash
02-airflow
│
├── Dockerfile
├── docker-compose.yaml
├── .env
│
└── data
    └── jph
        └── jupyterhub_config.py
```

### Dockerfile
```bash
python:3.14-slim
```
В контейнер устанавливаются:
- jupyterhub
- dockerspawner
- configurable-http-proxy
- sqlalchemy (<2)

### docker-compose.yaml
Docker Compose используется для запуска JupyterHub.

Основные параметры:
- порт 8000
- подключение docker.sock
- volume для хранения данных
- подключение конфигурационного файла JupyterHub

### Переменные окружения (.env)

Файл .env содержит ненастоящие секреты:
```bash
JPH_DUMMY_PASSWORD=jphadminpwd
```

### Сборка контейнера и запуск JupyterHub
```bash
docker compose build
```

```
docker compose up -d
```
![Скриншот](docs/04-jupyterhub/1.png)

### Проверка работы
После запуска сервис доступен по адресу:
```bash
http://localhost:8000
```
![Скриншот](docs/04-jupyterhub/2.png)
залогиниваемся
![Скриншот](docs/04-jupyterhub/3.png)
Всё работает, отлично!
  
# Задание 5 Mlservice
В рамках пятого задания был реализован полный цикл работы с моделью машинного обучения:

1. обучение модели на датасете `diabetes`
2. логирование параметров и метрик в **MLflow**
3. регистрация модели в **MLflow Model Registry**
4. загрузка зарегистрированной модели
5. развёртывание веб-сервиса на **FastAPI**
6. получение предсказания через REST API

---

# Архитектура решения

Проект состоит из двух основных частей:

## 1. Обучение и регистрация модели
Модель обучается в Jupyter Notebook и сохраняется в MLflow.

## 2. Веб-сервис FastAPI
Сервис загружает сохранённую модель и предоставляет endpoint для инференса.

Схема работы:

```text
Jupyter Notebook
      |
      v
   MLflow Server
      |
      v
Registered Model: diabets
      |
      v
mlflow.sklearn.load_model(...)
      |
      v
diabets_model.pkl
      |
      v
FastAPI service
      |
      v
POST /api/v1/predict
```

## Структура проекта
```text
05-mlservice/
├── Dockerfile
├── docker-compose.yaml
├── README.md
├── requirements.txt
├── model/
│   └── diabets_model.pkl
├── mlapp/
│   ├── __main__.py
│   └── server.py
└── research/
    └── train.ipynb
```

### Часть 1. Обучение и регистрация модели
```text
research/train.ipynb
```

В ноутбуке выполняются следующие шаги:
	•	загрузка датасета load_diabetes(scaled=False)
	•	разбиение на train/test
	•	обучение pipeline:
	•	StandardScaler
	•	RandomForestRegressor
	•	расчёт метрик:
	•	mae
	•	r2
	•	логирование параметров и метрик в MLflow
	•	логирование модели
	•	регистрация модели в Model Registry под именем: diabets

  После выполнения ноутбука в MLflow появился experiment:diabets-experiment
  и зарегистрированная модель:diabets / version 1
![Скриншот](docs/05-mlservice/1.png)
### Часть 2. Загрузка модели

После регистрации модель была загружена из MLflow и сохранена локально: model/diabets_model.pkl

### Часть 3. FastAPI сервис

Файл: mlapp/server.py

Сервис принимает 10 признаков пациента:
- age
- sex
- bmi
- bp
- s1
- s2
- s3
- s4
- s5
- s6

и возвращает предсказание модели.
Запуск сервиса

Из корня проекта:
```bash
python -m mlapp
```

Сервис становится доступен по адресу:
```text
http://localhost:8000
```

### Проверка работоспособности

Проверка модели:
![Скриншот](docs/05-mlservice/2.png)

Отлично, всё получилось!


# задание 6 - Логирование

ML-сервис был доработан с использованием `starlette-exporter`, чтобы Prometheus мог собирать метрики HTTP-запросов и состояния сервиса.

---

## Архитектура решения

```text
Client / curl
      |
      v
FastAPI ML service (localhost:8000)
      |
      v
   /metrics
      |
      v
Prometheus (localhost:9090)
      |
      v
Grafana (localhost:3000)
      |
      v
Dashboards
```
Дополнительно:
- node-exporter предоставляет системные метрики CPU и др.

Используемые сервисы

#### ML service

__FastAPI сервис с endpoint’ами__:
- GET /health
- POST /api/v1/predict
- GET /metrics

__Prometheus__
Собирает метрики с:
- самого себя
- ML сервиса
- node-exporter

__Grafana__
Используется для создания dashboard и визуализации метрик.

__node-exporter__
Предоставляет системные метрики, в том числе CPU.

#### Доработка FastAPI сервиса

В mlapp/server.py были добавлены:
```python
from starlette_exporter import PrometheusMiddleware, handle_metrics

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)
```

Это позволило Prometheus собирать метрики сервиса по пути:
```text
http://localhost:8000/metrics
```

docker-compose.yaml

В проект были добавлены сервисы:
- mlservice
- prometheus
- grafana
- node-exporter

Запуск всего стека:

```bash
docker compose up -d --build
```

Переменные окружения

Файл .env:

```text
GF_SECURITY_ADMIN_USER=admin
GF_SECURITY_ADMIN_PASSWORD=admin123
```

### Проверка Prometheus

Prometheus доступен по адресу:

```text
http://localhost:9090
```

![Скриншот](docs/06-monitoring/1.png)


### Проверка Grafana

Grafana доступна по адресу:

```text
http://localhost:3000
```
В Grafana был создан datasource:
![Скриншот](docs/06-monitoring/3.png)

### Dashboard
Был создан dashboard с графиками.
![Скриншот](docs/06-monitoring/4.png)

Отлично, всё получилось!

# __Задание 7: k8s__
