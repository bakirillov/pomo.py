import os
import json
import time
import argparse
import os.path as op
from tqdm import tqdm
from datetime import datetime
from pydub import AudioSegment
from pydub.playback import play

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--config",
        dest="config",
        action="store", 
        help="set config file", 
        default="default.json"
    )
    parser.add_argument(
        "-s", "--statistics",
        dest="statistics",
        action="store", 
        help="set destination for statistics", 
        default="statistics"
    )
    args = parser.parse_args()
    if not op.exists(args.statistics):
        os.makedirs(args.statistics)
    now = datetime.now().strftime("%d.%m.%Y-%H:%M:%S")
    this_session = now+".json"
    statistics = {
        "work": 0,
        "rest": 0,
        "config": args.config,
        "work_starts": [],
        "rest_starts": []
    }
    with open(args.config, "r") as ih:
        config = json.load(ih)
    statistics_path = op.join(args.statistics, this_session)
    sessions = config["sessions"]
    work = config["work"]
    short_rest = config["short_rest"]
    long_rest = config["long_rest"]
    work_sound = AudioSegment.from_mp3(config["work_sound"])
    rest_sound = AudioSegment.from_mp3(config["rest_sound"])
    for a in range(sessions):
        print("Starting Pomodoro session #"+str(a+1)+".")
        if a == 0:
            play(work_sound)
        print("Work!")
        statistics["work_starts"].append(
            datetime.now().strftime("%d.%m.%Y-%H:%M:%S")
        )
        for b in tqdm(list(range(work*60))):
            time.sleep(1)
        statistics["work"] += 1
        with open(statistics_path, "w") as oh:
            json.dump(statistics, oh)
        play(rest_sound)
        statistics["rest_starts"].append(
            datetime.now().strftime("%d.%m.%Y-%H:%M:%S")
        )
        play(rest_sound)
        if a != sessions-1:
            print("Rest!")
            for b in tqdm(list(range(short_rest*60))):
                time.sleep(1)
            statistics["rest"] += 1
            with open(statistics_path, "w") as oh:
                json.dump(statistics, oh)
            _ = input("Next session?")
            play(work_sound)
        else:
            print("Long rest!")
            for a in tqdm(list(range(long_rest*60))):
                time.sleep(1)
            statistics["rest"] += 1
            with open(statistics_path, "w") as oh:
                json.dump(statistics, oh)
            play(work_sound)