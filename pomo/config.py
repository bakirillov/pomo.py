import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


@dataclass
class Config:
    work_time: int
    short_rest: int
    long_rest: int
    sessions: int
    work_sound: Path
    rest_sound: Path


config = Config(
    int(os.getenv("POMO_WORK_TIME", default="25")),
    int(os.getenv("POMO_SHORT_REST", default="5")),
    int(os.getenv("POMO_LONG_REST", default="15")),
    int(os.getenv("POMO_SESSIONS", default="2")),
    Path(os.getenv("POMO_WORK_SOUND", "../work.mp3")),
    Path(os.getenv("POMO_REST_SOUND", "../work.mp3")),
)
