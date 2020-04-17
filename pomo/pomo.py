import argparse
import json
import os
import os.path as op
import time
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

import fire
from loguru import logger
from pydub import AudioSegment
from pydub.playback import play
from tqdm import tqdm

from pomo.config import config


class Session:
    def __init__(self, duration, statistics, stat_path, sound):
        self.sound = sound
        self.stat_path = stat_path
        self.duration = duration
        self.statistics = statistics

    def write_stat(self):
        with self.stat_path.open("w") as oh:
            json.dump(self.statistics, oh)
        play(self.sound)

    def wait(self):
        for _ in tqdm(range(self.duration), total=self.duration):
            time.sleep(1)

    def start(self):
        raise NotImplementedError()


class WorkSession(Session):
    def start(self):
        logger.opt(colors=True).info("<g>Work!</>")
        self.statistics["work_starts"].append(datetime.now().strftime("%d.%m.%Y-%H:%M:%S"))

        # self.wait()

        self.statistics["work"] += 1
        self.write_stat()


class ShortRestSession(Session):
    def start(self):
        logger.opt(colors=True).info("<cyan>Rest!</>")
        # self.wait()

        self.statistics["rest"] += 1
        self.write_stat()


class LongRestSession(Session):
    def start(self):
        logger.opt(colors=True).info("<cyan>Long rest!</>")
        # self.wait()

        self.statistics["rest"] += 1
        self.write_stat()


def main(statistics: str = "statistics"):
    """

    :param statistics: set destination for statistics
    """
    stat_path = Path(statistics)

    if not stat_path.exists():
        os.makedirs(str(stat_path))

    now = datetime.now().strftime("%d.%m.%Y-%H:%M:%S")
    this_session = now + ".json"
    statistics = {
        "work": 0,
        "rest": 0,
        "config": str(config),
        "work_starts": [],
        "rest_starts": [],
    }

    statistics_path: Path = stat_path / str(this_session)

    work_sound = AudioSegment.from_mp3(config.work_sound)
    rest_sound = AudioSegment.from_mp3(config.rest_sound)

    work_session = WorkSession(
        duration=config.work_time * 60,
        statistics=statistics,
        stat_path=statistics_path,
        sound=work_sound,
    )
    short_rest_session = ShortRestSession(
        duration=config.short_rest * 60,
        statistics=statistics,
        stat_path=statistics_path,
        sound=work_sound,
    )
    long_rest_session = LongRestSession(
        duration=config.long_rest * 60,
        statistics=statistics,
        stat_path=statistics_path,
        sound=work_sound,
    )

    for a in range(config.sessions):
        if a == 0:
            play(work_sound)
        logger.info("Starting Pomodoro session #{}", a + 1)
        # Work session
        work_session.start()

        statistics["rest_starts"].append(datetime.now().strftime("%d.%m.%Y-%H:%M:%S"))
        play(rest_sound)

        if a != config.sessions - 1:
            short_rest_session.start()
            input("Next session?")
        else:
            long_rest_session.start()


if __name__ == "__main__":
    fire.Fire(main)
