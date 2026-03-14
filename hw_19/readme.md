
## ДЗ 19 —  DVC
### Дисциплина: DataOps
__Тема: DVC__
### Цель - научиться локально разворачивать lakefs сервер, создавать в нем репозитории и версионировать датасеты.

### Архитектура решения

В рамках задания была поднята локальная инфраструктура:

- **PostgreSQL** — метаданные lakeFS
- **MinIO** — S3-совместимое объектное хранилище
- **lakeFS** — система версионирования данных
- **lakectl** — CLI для работы с lakeFS

```bash
docker compose up -d
```
Для начала поднимаем Postgres
![Скриншот](screenshots/1.png)

Далее поднимаем Minio
![Скриншот](screenshots/2.png)

Заходим в Minio
![Скриншот](screenshots/3.png)

- MinIO Console -  http://localhost:9001
- MinIO S3 API - http://localhost:9000

Создаём бакет lakefs
![Скриншот](screenshots/4.png)

Поднимаем Lakefs
![Скриншот](screenshots/5.png)

При первом запуске был выполнен setup:
```bash
http://localhost:8000/setup
```
В процессе настройки были созданы:
	•	Access Key
	•	Secret Key
  
Вводим данные и получаем credidentials
![Скриншот](screenshots/6.png)
![Скриншот](screenshots/7.png)
![Скриншот](screenshots/8.png)

Эти ключи использовались для настройки CLI

После создаём репозиторий
![Скриншот](screenshots/9.png)
![Скриншот](screenshots/10.png)

Была создана новая ветка
```bash
featone
```
Она используется как рабочая ветка для изменения данных.

![Скриншот](screenshots/11.png)

В репозиторий был добавлен новый файл:
```bash
echo "hello lakefs" > firstrepo/data.txt
```

Изменения были зафиксированы в lakeFS:
![Скриншот](screenshots/12.png)

После compare main и featone был сделан merge
![Скриншот](screenshots/13.png)

Итоговая структура репозитория

В ветке main находятся:
```bash
README.md
data.txt
data/
images/
lakes.parquet
```
![Скриншот](screenshots/14.png)

Отлично, всё получилось!
