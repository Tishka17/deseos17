## Deseos17 (Lista de deseos)

This project is a demo implementation of "Clean architecture" in Python.

* [Domain specification](docs/domain.md)
* [Implementation details](/docs/implementation.md)
* [Implementation log](/docs/implementation_log.md)

### Running code:

1. Install

```sh
pip install -e .
```

2. Run bot preview

```sh
aiogram-dialog-preview deseos17.main.bot:get_dispatcher_preview
```

3. Provide env variables:

* `BOT_TOKEN` - your telegram bot token
* `JWT_SECRET` - some secret long string to work with JWT tokens
* `LOGIN_URL` - url in format `https://yourdomain/login` which is set in your telegram bot for auth widget

4. Run fastapi

```sh
uvicorn deseos17.main.web:app
```
5. Run bot

```sh
python -m deseos17.main.bot
```