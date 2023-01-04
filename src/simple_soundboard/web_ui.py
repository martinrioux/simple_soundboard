
import sys
from fastapi import Depends, FastAPI, Request, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import pkg_resources
import asyncio
import ujson
import uvicorn
import secrets
import shutil
import os
from glob import glob
from dataclasses import dataclass, asdict, field
from simple_soundboard.sound_engine import SoundEngine

CONFIG_FOLDER = os.path.expanduser("~") + "/simple_soundboard/"
MEDIA_FOLDER = os.path.expanduser("~") + "/simple_soundboard/media/"
CONFIG_FILE = CONFIG_FOLDER + "config.json"


@dataclass
class FileInfo:
    filename: str
    volume: float = 0.5
    is_music: bool = False
    is_folder: bool = False
    start_time: float = 0
    stop_time: float = -1
    loop_playback: bool = False
    mqtt_topic: str = None
    icon: str = ""


@dataclass
class FolderInfo:
    content: list[FileInfo] = field(default_factory=list)


if not os.path.exists(CONFIG_FILE):
    os.makedirs(CONFIG_FOLDER, exist_ok=True)
    shutil.copy2(pkg_resources.resource_filename(__name__, "config.json"), CONFIG_FILE)

if not os.path.exists(MEDIA_FOLDER):
    os.makedirs(MEDIA_FOLDER, exist_ok=True)


sound_engine = SoundEngine()


security = HTTPBasic()
app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory=pkg_resources.resource_filename(__name__, "static")),
    name="static",
)


def get_config():
    """
    Returns config
    """
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        config = file.read()
        file.close()
    return ujson.loads(config)


def init_folder_info_file(info_file_path):
    """
    Init a folder content file
    """
    with open(info_file_path, "w") as f:
        f.write(ujson.dumps(asdict(FolderInfo())))


def get_folder_info(relative_folder_path) -> FolderInfo:
    """
    Returns folder info
    """
    folder_info_file = f"{MEDIA_FOLDER}{relative_folder_path}/folder_info.json"
    if not os.path.exists(folder_info_file):
        init_folder_info_file(folder_info_file)

    try:
        with open(folder_info_file, "r") as f:
            folder_info = FolderInfo(**ujson.loads(f.read()))
            for i in range(len(folder_info.content)):
                folder_info.content[i] = FileInfo(**folder_info.content[i])
    except ValueError:
        folder_info = FolderInfo()
        save_folder_info(relative_folder_path, folder_info)

    return folder_info

def save_folder_info(relative_folder_path, folder_info):
    folder_info_file = f"{MEDIA_FOLDER}{relative_folder_path}/folder_info.json"
    with open(folder_info_file, "w") as f:
        f.write(ujson.dumps(asdict(folder_info), indent=4))
        f.close()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    config = get_config()
    username_test = secrets.compare_digest(credentials.username, config["username"])
    password_test = secrets.compare_digest(credentials.password, config["password"])
    credential_test = username_test and password_test

    if not credential_test:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get('/api/get_config')
async def api_get_config(username: str = Depends(get_current_username)):
    """
    Returns config
    """
    config = get_config()
    return JSONResponse(config)


@app.post('/api/get_folder_info')
async def api_get_folder_info(request: Request, username: str = Depends(get_current_username)):
    """
    Returns folder info
    """
    current_folder = await request.json()
    current_folder = current_folder["current_folder"]

    config = get_folder_info(current_folder)
    initial_config = ujson.dumps(asdict(config))
    all_files = glob(f"{MEDIA_FOLDER}{current_folder}/*", recursive=False)

    for f in all_files:
        filename = f.split(MEDIA_FOLDER)[1]
        if any([x.filename == filename for x in config.content]):
            continue

        is_folder = os.path.isdir(f)

        if is_folder:
            print("folder",filename)
            config.content.append(FileInfo(filename, is_folder=True))
        else:
            extension = os.path.splitext(f)[1]
            if extension not in [".mp3", ".ogg"]:
                continue
            config.content.append(FileInfo(filename))

    filtered_folder_info = FolderInfo()
    for file in config.content:
        if not os.path.exists(f"{MEDIA_FOLDER}{file.filename}"):
            continue
        if any([x.filename == file.filename for x in filtered_folder_info.content]):
            continue
        filtered_folder_info.content.append(file)

    final_config = ujson.dumps(asdict(filtered_folder_info))
    if initial_config != final_config:
        save_folder_info(current_folder, filtered_folder_info)

    return JSONResponse(asdict(filtered_folder_info))


@app.post('/api/upload_file')
async def api_upload_file(request: Request, username: str = Depends(get_current_username)):
    """
    Upload a file
    """
    data = await request.body()
    filename = request.headers.get("filename")
    current_folder = request.headers.get("current_folder")

    with open(f"{MEDIA_FOLDER}{current_folder}/{filename}", "wb") as f:
        f.write(data)
        f.close()

    return JSONResponse({"success": True})


@app.post('/api/delete_file')
async def api_delete_file(request: Request, username: str = Depends(get_current_username)):
    """
    Delete a file
    """
    file_info = await request.json()
    file_info = FileInfo(**file_info["file"])

    os.remove(f"{MEDIA_FOLDER}{file_info.filename}")

    return JSONResponse({"success": True})


@app.post('/api/play_sound')
async def api_play_sound(request: Request, username: str = Depends(get_current_username)):
    """
    Plays a sound
    """
    file_info = await request.json()
    file_info = FileInfo(**file_info["file"])

    if file_info.is_music:
        sound_engine.play_music(f"{MEDIA_FOLDER}{file_info.filename}", file_info.volume, file_info.loop_playback)
    else:
        sound_engine.play_sound(f"{MEDIA_FOLDER}{file_info.filename}", file_info.volume)
    return JSONResponse({"success": True})


@app.get('/api/stop_all_sounds')
async def api_stop_all_sounds(request: Request, username: str = Depends(get_current_username)):
    """
    Stops all playing sounds
    """
    sound_engine.stop_all_sounds()
    return JSONResponse({"success": True})


@app.get('/api/fadeout_music')
async def api_fadeout_music(request: Request, username: str = Depends(get_current_username)):
    """
    Fadeout Music
    """
    sound_engine.fadeout_music()
    return JSONResponse({"success": True})


@app.post('/api/save_folder_info')
async def api_save_folder_info(request: Request, username: str = Depends(get_current_username)):
    """
    Save current folder Info
    """

    info = await request.json()
    current_folder = info["current_folder"]
    folder_info = FolderInfo(**info["folder_info"])
    for i in range(len(folder_info.content)):
        folder_info.content[i] = FileInfo(**folder_info.content[i])

    save_folder_info(current_folder, folder_info)
    return JSONResponse({"success": True})

@app.get("/{full_path:path}", include_in_schema=False)
def root(request: Request, full_path: str, username: str = Depends(get_current_username)):
    index_file = pkg_resources.resource_string(__name__, "./index.html").decode("utf-8", "ignore")
    return HTMLResponse(index_file)

def start():
    sound_engine.init()

    uvicorn.run(app, host='0.0.0.0', port=get_config()["port"])
    return sys.exit()

if __name__ == "__main__":
    start()
