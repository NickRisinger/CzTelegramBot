# Инструкция для настройки проекта

## Настройка виртуального окружения

### Создание виртуального окружения
```shell
python -m venv venv
```

### Установка зависимостей
```shell
pip install -r requirements.txt
```

### Установка библиотеки для подписи строк
```shell
pip install pywin32
```

### Обновление библиотеки для сборки
```shell
pip install --upgrade setuptools
```

## Настройка параметров окружения

1. Создать файл .env
2. Заполнить данными:
```text
BOT_TOKEN=""
BOT_SUPPORT_GROUP_ID=""
BOT_NOTIFY_GROUP_ID=""
DATABASE_FILE="file:../data/database.sqlite3"
```


## Настройка базы данных и статичных файлов

### Создание базы данных
```shell
prisma db push
```

### Генерация клиента
```shell
prisma generate
```

### Различные команды
```shell
prisma migrate dev --name ""

prisma generate
```

## Запуск проекта

### Запуск
```shell
python ./main.py
```