# Grants API

Objective of this API is to use Clean architecture based FASTAPI application which can be used across organiastions to run thier internal grants or challenges

## Prerquistives
- Python - 3.11
- Poetry 
- VS Code or PyCharm

## Installation command
1. The following Poetry commands are what you need to start working with this project
```shell
   poetry add fastapi
   poetry update 
   poetry run
```
2. To run `Alembic (SQL Alchemy)` migrations
```shell
   
   /* to create migrations */
   alembic revision --autogenerate -m "simplied relationships"
   
   /* To run migrations */
   alembic upgrade +1  
```
3. To run tests using `pytest` you only need to write functions with `test_` prefix
4. To run the application you will need a ASGI supported webserver
```shell
uvicorn main:app -p 8000 --reload
```

The `--reload` option allows the application to reload as you do your changes.

for more indepth architecture discussion you can go to the `docs` folder