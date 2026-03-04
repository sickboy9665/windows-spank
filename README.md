# Laptop Spank (Windows)

A fun tool that reacts when you slap your laptop.

# Inspired from spank https://github.com/taigrr/spank
Added the same sounds to this project. Now spank your windows laptop as well!!

## How it works

The script continuously listens to your microphone input. When you hit or slap your laptop, it detects the sudden audio volume spike. Depending on the amplitude of the spike, it classifies the hit into three levels:
* **Light**
* **Medium**
* **Hard**

It then randomly selects a sound file from the corresponding folder and plays it immediately. There is a built-in ~1 second cooldown so sounds don't spam.

## Installation

1. Clone or download this project.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Adding custom sounds

The script reads available sound files dynamically from the `sounds/` folders. It supports `.mp3` or `.wav` formats. 

To add your own custom sounds:
1. Place light hit sounds in `sounds/light/`
2. Place medium hit sounds in `sounds/medium/`
3. Place hard hit sounds in `sounds/hard/`

If a folder is empty, the program will just skip playing a sound without crashing.

## Usage

Run the program from your terminal:

```bash
python spank.py
```

### Preferred Spank
You can optionally specify a preferred spank intensity (light, medium, or hard). Any detected hit will play the sound from that specific folder:

```bash
python spank.py --spank hard
```

You should see:
```text
Listening... slap your laptop.
```
Now give your laptop a slap!
