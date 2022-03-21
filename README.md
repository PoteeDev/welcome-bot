# Potee Welcome Bot

## Запуск в докере

### Сборка

```
docker build -t welcome-bot .
```

### Запуск

Чтобы запустить бот, нужно добавить переменную окружения`BOT_TOKEN`. Для этого можно создать файл `.env`

```
docker run --rm --env-file=.env -v $PWD:/usr/src/app welcome-bot
```

