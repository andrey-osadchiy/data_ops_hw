## ДЗ 18 —  DB migrations через yoyo
### Дисциплина: DataOps
__Тема: Работа с БД в ML-проектах__
Цель работы:
- научиться писать миграции баз данных в ML проектах на примере библиотеки yoyo-migrations

  
## DZ18 — DB migrations with yoyo

### Запускаем DB
docker compose up -d

### Создаём миграцию
```bash
export $(cat .env | xargs)
python -m yoyo apply --database "$DB_URL" -b ./migrations
```
![Скриншот](screenshots/3.png)
### Rollback откатываем
```bash
python -m yoyo rollback --database "$DB_URL" -b ./migrations
```
![Скриншот](screenshots/4.png)
### Создаём новую миграцию
```bash
cat > migrations/002_add_lastname.py <<'PY'
from yoyo import step

__depends__ = {"001_create_users"}

steps = [
    step(
        """
        ALTER TABLE users
        ADD COLUMN lastname VARCHAR(100);
        """,
        """
        ALTER TABLE users
        DROP COLUMN lastname;
        """
    )
]
PY
```

проверяем её
```bash
export $(cat .env | xargs)
python -m yoyo apply --database "$DB_URL" -b ./migrations
docker exec -it dz18-postgres psql -U mluser -d mldb -c "\d users"
```
откатываем и проверяем
![Скриншот](screenshots/5.png)
![Скриншот](screenshots/6.png)
