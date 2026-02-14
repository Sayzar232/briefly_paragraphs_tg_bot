import asyncio
import logging
from aiohttp import web

from aiogram import Bot, Dispatcher, types

from config import TOKEN, WEBHOOK_URL, WEBHOOK_PATH, APP_HOST, APP_PORT, ADMIN_TOKEN
from callbacks_handler import router
from message_handler import router as message_router
from database import init_db, get_user_count

logging.basicConfig(level=logging.INFO)


bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_routers(router, message_router)


async def handle_webhook(request: web.Request) -> web.Response:
    if request.content_type != 'application/json':
        return web.Response(status=415, text='Unsupported Media Type')

    data = await request.json()
    update = types.Update(**data)
    await dp._process_update(bot, update)
    return web.Response(text='OK')


async def health_check(request):
    return web.Response(text="OK", status=200)


async def admin_handler(request: web.Request) -> web.Response:
    # simple token-based protection (use env ADMIN_TOKEN)
    token = request.query.get('token') or request.headers.get('X-ADMIN-TOKEN')
    if token != ADMIN_TOKEN:
        return web.Response(status=403, text='Forbidden')

    count = await get_user_count()
    return web.Response(text=f"users_count: {count}")


async def on_startup(app: web.Application):
    # initialize DB
    await init_db()

    # register webhook with Telegram if WEBHOOK_URL is configured
    if WEBHOOK_URL:
        full_url = WEBHOOK_URL.rstrip('/') + WEBHOOK_PATH
        await bot.set_webhook(full_url, allowed_updates=["message", "callback_query"])
        logging.info(f"Webhook set to {full_url}")
    else:
        logging.warning("WEBHOOK_URL not set — webhook won't be configured.")


async def on_cleanup(app: web.Application):
    try:
        await bot.delete_webhook()
    finally:
        await bot.session.close()


def create_app() -> web.Application:
    app = web.Application()

    # webhook route
    path = WEBHOOK_PATH if WEBHOOK_PATH.startswith('/') else '/' + WEBHOOK_PATH
    app.router.add_post(path, handle_webhook)

    app.router.add_get("/", health_check)
    # admin route
    app.router.add_get('/admin', admin_handler)

    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)
    return app


if __name__ == '__main__':
    if not TOKEN:
        raise RuntimeError('TOKEN is not set in environment')

    app = create_app()
    web.run_app(app, host=APP_HOST, port=APP_PORT)