# Задание №47 — ML-модель Titanic в Docker

Проект для задания 47: контейнеризация модели Random Forest из задания 46. REST API реализован с FastAPI.

## Содержимое
- `Dockerfile` — сборка образа Python 3.11
- `app.py` — загрузка модели и методы `/health`, `/predict`
- `requirements.txt` — фиксированные зависимости
- `titanic_random_forest.joblib` — обученная модель из задания 46 (необходимый бинарный артефакт)

> Для полной сборки необходимо добавить `titanic_random_forest.joblib` в корень репозитория. Без этого файла Docker-сборка не завершится.

## Сборка и запуск

```bash
docker build -t titanic-ml:1.0 .
docker run --rm -p 8000:8000 titanic-ml:1.0
```

Документация API: http://localhost:8000/docs

Тестовый запрос:

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"Pclass":3,"Age":25,"SibSp":0,"Parch":0,"Fare":8.0,"Sex":"male","Embarked":"S"}'
```

## Вывод

Модель Random Forest из задания 46 предоставляется через REST API в Docker-контейнере. Контейнер изолирует зависимости и обеспечивает одинаковое окружение для инференса на разных компьютерах.
