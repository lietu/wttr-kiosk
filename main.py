import os
import shutil
import sys
from pathlib import Path
from subprocess import run  # nosec
from time import time, sleep

import requests
from loguru import logger

import settings

if sys.platform == "win32":
    PATH_PREFIX = os.environ["TEMP"] + "\\"
else:
    PATH_PREFIX = "/tmp/"

TEMP_PATH = PATH_PREFIX + "temp.png"
BACKGROUND_PATH = PATH_PREFIX + "background.png"
WTTR_PATH = PATH_PREFIX + "wttr.png"
LAST_BG = 0
LAST_WTTR = 0


def download(src, dst):
    logger.info("Downloading {src} to {dst}", src=src, dst=dst)
    r = requests.get(src, stream=True)
    r.raise_for_status()
    if r.status_code == 200:
        with open(dst, "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)


def download_background():
    global LAST_BG

    # If the image has already been downloaded recently
    since = time() - settings.UPDATE_BACKGROUND
    if since < settings.UPDATE_BACKGROUND and Path(BACKGROUND_PATH).exists():
        return

    if settings.BACKGROUND_TYPE == "mjpeg":
        logger.info(
            "Grabbing {src} frame to {dst}",
            src=settings.BACKGROUND_URL,
            dst=BACKGROUND_PATH,
        )
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            settings.BACKGROUND_URL,
            "-vframes",
            "1",
            "-q:v",
            "2",
            BACKGROUND_PATH,
        ]
        run(cmd, check=True)
    elif settings.BACKGROUND_TYPE == "jpg":
        download(settings.BACKGROUND_URL, BACKGROUND_PATH)
    else:
        raise Exception(f"Unknown background type {settings.BACKGROUND_TYPE}")

    LAST_BG = time()


def download_wttr():
    global LAST_WTTR

    # If the image has already been downloaded recently
    since = time() - settings.UPDATE_WTTR
    if since < settings.UPDATE_WTTR and Path(WTTR_PATH).exists():
        return

    download(settings.WTTR_URL, WTTR_PATH)
    LAST_WTTR = time()


def combine_images():
    logger.info("Combining images to {out}", out=settings.OUTPUT_IMAGE)
    cmd = [
        "convert",
        BACKGROUND_PATH,
        WTTR_PATH,
        "-geometry",
        "+50+50",
        "-composite",
        TEMP_PATH,
    ]
    run(cmd, check=True)
    shutil.move(Path(TEMP_PATH).absolute(), Path(settings.OUTPUT_IMAGE).absolute())


def main(wait=True):
    start = time()
    download_background()
    download_wttr()
    combine_images()
    elapsed = time() - start
    logger.info("New image generated in {elapsed:.3f}s", elapsed=elapsed)

    if wait:
        wait_time = max(0.1, settings.UPDATE_SECONDS - elapsed)
        logger.debug("Waiting {wait}s", wait=wait_time)
        sleep(wait_time)


if __name__ == "__main__":
    oneshot = len(sys.argv) > 0 and "--oneshot" in sys.argv
    while True:
        try:
            main(not oneshot)
            if oneshot:
                break
        except Exception as e:
            logger.exception("Caught exception from main(): " + str(e))
