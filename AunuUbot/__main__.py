import asyncio
import signal
import tornado.ioloop
import tornado.platform.asyncio
from pyrogram import Client
from AunuUbot import *


async def shutdown(sig, loop):
    print(f"Received exit signal {sig.name}...")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    print("Cancelling outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()


async def main():
    await bot.start()
    for _ubot in await get_userbots():
        ubot_ = Ubot(**_ubot)
        try:
            await asyncio.wait_for(ubot_.start(), timeout=10)
        except asyncio.TimeoutError:
            await remove_ubot(int(_ubot["name"]))
            print(f"[\u026a\u0274\u0493\u1d0f]: {int(_ubot['name'])} \u1d1b\u026a\u1d05\u1d00\u1d0b \u1d05\u1d00\u1d18\u1d00\u1d1b \u1d0d\u1d07\u0280\u1d07s\u1d18\u1d0f\u0274\u1d07")
        except Exception:
            await remove_ubot(int(_ubot["name"]))
            print(f"[\u026a\u0274\u0493\u1d0f]: {int(_ubot['name'])} \u1d03\u1d07\u0280\u029c\u1d00s\u026a\u029f \u1d05\u026a \u029c\u1d00\u1d18\u1d1c s")
    await bash("rm -rf *session*")
    await asyncio.gather(loadPlugins(), installPeer(), expiredUserbots())
    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()

    def _make_handler(s):
        def handler():
            asyncio.create_task(shutdown(s, loop))
        return handler

    for s in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(s, _make_handler(s))

    try:
        await stop_event.wait()
    except asyncio.CancelledError:
        pass
    finally:
        await bot.stop()


if __name__ == "__main__":
    tornado.platform.asyncio.AsyncIOMainLoop().install()
    loop = tornado.ioloop.IOLoop.current().asyncio_loop
    loop.run_until_complete(main())
