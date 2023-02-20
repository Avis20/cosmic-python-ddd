

# check db connect

```
docker exec -it cosmic-python-ddd_cosmic-app_1 sh
PGPASSWORD=cosmic-pass psql -h cosmic-db -p 5432 -U cosmic-user -d cosmic
```

# Remove pycache
`find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf`


# alembic

docker-compose run --no-deps --rm cosmic-db_migrate

poetry run alembic upgrade head

poetry run alembic revision --autogenerate -m "test"

```
docker-compose run --no-deps --rm cosmic-db_migrate poetry run alembic revision --autogenerate -m "test"
```
