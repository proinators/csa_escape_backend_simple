from enum import Enum
from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Route
import socketio
import uvicorn
import logging
from consts import Consts

class GameStatus(Enum):
    intro = "intro"
    long = "long"
    short = "short"

class BGMStatus(Enum):
    clear = "clear"
    main = "main"
    hint1 = "hint1"
    hint2 = "hint2"
    hint3 = "hint3"

middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'])
]

consts = Consts()
current_game_status = GameStatus.intro
current_bgm_status = BGMStatus.clear

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

sio = socketio.AsyncServer(async_mode='asgi', logger=True, engineio_logger=True, cors_allowed_origins='*')
socketio_app = socketio.ASGIApp(sio)

async def index(request):
    return HTMLResponse("<h1>Video & BGM Control API</h1>")

app = Starlette(debug=False, routes=[
    Route('/', index),
], middleware=middleware)

app.mount('/socket.io', socketio_app)

@sio.event
def connect(sid, environ):
    print("connect ", sid)

async def status_change(status: GameStatus):
    global current_game_status
    current_game_status = status
    await sio.emit("display", status.name)
    return HTMLResponse(f'Display status set to {status.name}.')

async def bgm_change(status: BGMStatus):
    global current_bgm_status
    current_bgm_status = status
    await sio.emit("bgm", status.name)
    return HTMLResponse(f'BGM set to {status.name}.')

@app.route('/admin/status/{new_status}')
async def admin_status(request):
    try:
        new_status = GameStatus._member_map_[request.path_params['new_status']]
        return await status_change(new_status)
    except Exception as e:
        return HTMLResponse('Invalid display status')

@app.route('/admin/bgm/{new_status}')
async def admin_bgm(request):
    try:
        new_status = BGMStatus._member_map_[request.path_params['new_status']]
        return await bgm_change(new_status)
    except Exception as e:
        return HTMLResponse('Invalid BGM status')

@app.route('/state')
async def state(request):
    return JSONResponse({
        "display_status": current_game_status.name,
        "bgm_status": current_bgm_status.name,
    }, 200)

@app.route('/admin/list')
async def admin_dashboard(request):
    return JSONResponse([
        {
            "heading": "Video Control",
            "actions": [
                {
                    "name": "Intro",
                    "endpoint": "admin/status/intro"
                },
                {
                    "name": "Long Video",
                    "endpoint": "admin/status/long"
                },
                {
                    "name": "Short Video",
                    "endpoint": "admin/status/short"
                }
            ]
        },
        {
            "heading": "BGM Control",
            "actions": [
                {
                    "name": "Clear BGM",
                    "endpoint": "admin/bgm/clear"
                },
                {
                    "name": "Main Theme",
                    "endpoint": "admin/bgm/main"
                },
            ]
        }
    ])

if __name__ == "__main__":
    config = uvicorn.Config("main:app", host=("127.0.0.1" if consts.IS_DEBUG == '1' else "0.0.0.0"), port=consts.PORT, log_level="info")
    server = uvicorn.Server(config)
    server.run()