# Wttr Kiosk

Kiosk for [wttr.in](https://wttr.in) weather reports.

Intended for use with a Raspberry Pi (tested on 3B+) with a [motion](https://motion-project.github.io) based camera stream as the background, but can probably work for other circumstances as well.

I used a [WaveShare 3.5" RPi LCD (A)](https://www.waveshare.com/wiki/3.5inch_RPi_LCD_(A)) display with mine. You can choose to use HDMI, or other displays.

This kiosk package combines:

- [chilipie-kiosk](https://github.com/futurice/chilipie-kiosk) to turn your Raspberry Pi into a solid kiosk machine - it
  automatically boots into a full screen browser window
- A small service to automatically update a picture with a recent weather broadcast on a background of your choice (incl. live camera feed, which it was designed for)
- A simple webpage for you to open in that browser that refreshes that image every second

It doesn't attempt to be particularly elegant, but it does the job and should be easily customizable.

## Setup on Raspberry Pi

Here's the rough set of steps I used to install everything:

0. (Optional) [Set up Motion](https://www.instructables.com/How-to-Make-Raspberry-Pi-Webcam-Server-and-Stream-/) with a webcam - I set up mine for 512x288 @ 10 FPS output on a separate RPi2 near a window, and wttr-kiosk on a RPi3 near my entrance
1. Install [chilipie-kiosk](https://github.com/futurice/chilipie-kiosk) - download the latest release and burn it on an SD card with [balenaEtcher](https://www.balena.io/etcher/)
2. Boot the Raspberry Pi
3. Set up networking (or use the [automatic WiFi](https://github.com/futurice/chilipie-kiosk#automatic-wifi-setup) guide for chilipie)
4. Expand the partition to full disk via `raspi-config`
5. Update packages `sudo apt-get update && sudo apt-get upgrade && sudo apt-get clean`
6. Fix autologin: `sudo ln -fs /etc/systemd/system/autologin@.service /etc/systemd/system/getty.target.wants/getty@tty1.service`
7. (OPTIONAL) Install LCD drivers if not using HDMI out (check manufacturer guide) and then install `fbturbo`: `sudo apt-get install xserver-xorg-video-fbturbo`
8. [Install a recent version of Python](https://gist.github.com/dschep/24aa61672a2092246eaca2824400d37f) - I recommend using [latest Python](https://www.python.org/downloads/source/)
9. Get Wttr Kiosk source: `wget -O wttr-kiosk.zip https://github.com/lietu/wttr-kiosk/archive/refs/heads/master.zip`
10. Extract it: `unzip wttr-kiosk.zip; cd wttr-kiosk-master`
11. Configure it: `nano settings.py`
12. Setup wttr-kiosk: `bash setup.sh`
13. Open up `index.html` in your browser, e.g. via `file:///home/pi/wttr-kiosk-master/index.html`

Check out [wttr.in/:help](https://wttr.in/:help) for help with the weather image URLs.

## End result

[![Video of wttr kiosk in action](https://img.youtube.com/vi/lZAP1OEKK4s/0.jpg)](https://www.youtube.com/watch?v=lZAP1OEKK4s)

Click the image for video.

## License

Everything in this repository is licensed under the BSD 3-clause -license. This depends on other components from other people who license their code differently.
