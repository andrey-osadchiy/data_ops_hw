db.migration.new:
	python -m yoyo new migrations -m "$(name)"

db.migrate:
	python -m yoyo apply --database ${DB_URL} -b ./migrations

db.rollback:
	python -m yoyo rollback --database ${DB_URL} -b ./migrations
