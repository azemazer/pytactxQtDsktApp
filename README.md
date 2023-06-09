# pytactxQtDsktApp aka TF2 Pub Simulator

PytactX is a virtual arena created by jusdeliens.com where you can code your own AI to fight with other robot.
TF2 Pub Simulator is a desktop app which lets you control the PytactX agent with a graphical interface. The theme is TF2 :)

## Required

Python 3
pip install paho-mqtt pillow

## Installation

No installation yet. Run "App.py".

## How to use

1. Go to https://play.jusdeliens.com/login/
2. Login with your username (it can be anything), and enter the arena
3. Click on the arena you want to join
4. Launch app.py
5. On the connect tab, put your username in "Nickname", the name of the arena you chose in "Arena", and "demo" in "Password"
6. You now control the bot in the arena! Watch him beat his ennemies.

## As a user, you can:

On the "Connect tab"

    - Connect to an arena

Once connected, on the Control tab

    - See your heavy sprite and his orientation
    - Move up, down, left or right
    - Toggle shoot
    - See your HP
    - See your ammo
    - Toggle autopilot*
    - See your score

The windows are also resizable.
If you have access to the real-life jusdelien bots, you can hear it play various piece of TF2 music when you frag, die, respawn or take damage.

## Autopilot

Uses a FSM. Diagram [here.](https://mermaid.live/edit#pako:eNqlVF9v2jAQ_yonP07AlsSEkodJXammPXUafYAte7DIAdYSO7IdOlbx3XdJuiWAO5AWKUp0d78_ujv7ma10hixhQE-qrBMOZ1JsjCiGuzBVdfjbm-8wHL6HL7jaoqE3gXkpnpRt0w2mS8JzGz5CapVhqrrEC6YO9-vPMMFxro116TAhXUGiGZTaSie1Ah8k7CCRBxJ6IFEH4R5I5IHwnm8PhHeQQ78XbRdq6P1O5BU15l5hIdHeaesSmGm0sNYGd2ha0KH9dB2vsdS2BDJC-ZKPaAqphNPmQ5XneyJFhytnQUCun2BFQoAkuu9P9ATknSuuqrJ2u_-s7a3KPpLXR03__zDa0c6VLNH0zRSYyaq46KcFXjTUG-txvCltvTaxBVl_MBKVo54bQ2bqHi1AWlAozJ--XyZaeomWPqIL8g3zfKu1s03Ng_rk7CIBUgXTbpaXa3kt1_IVrjPN65p1u6EAKE37pDY0G6kglwpBr8HKzda9LrC8ronXCbxs3Onqntxed1th6WQ2G0ZnxoqypOlYeAuzvwfobNv-i6OzcXJOvTK9GjZgBZUImdEd3Sx8ytwWC0xZQr-ZMD9SlqoD1YnK6flerVjiTIUDVpVZd5mzZC1yS9FSKJY8s58sGfJ30Wg8Gd9MpxGfhHHA-YDtKT4J-Gga8CgOJ-M4jMf8MGC_tCaOYDTlQRxH4zCIeHjDedwQfm2SterhN4dyAhk)

## Graphics

Link to the [figma model](http://www.figma.com/file/vrtPgi1lMvBhYUB0aIbdb9/Untitled?type=design&amp;node-id=0%3A1&amp;t=xdE9ul4PewLjq9gt-1).

## Authors

Anything from the J2L folder: **jusdeliens.com**

Rest of the code: **azemazer**

Everything which references TF2 is property of **valve**

Heavy top down view model: **Brokenphillip**
