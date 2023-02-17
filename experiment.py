import json
import warnings
import os.path as op
import time
import pandas as pd
import numpy as np
from functions import generate_trials
from psychopy import core
from psychopy import visual
from psychopy import monitors
from psychopy import gui
from psychopy import event
from datetime import datetime


warnings.filterwarnings("ignore")

with open("settings.json") as json_file:
    params = json.load(json_file)

angles = params["angles"]
reps_free = params["repetitions_free_choice"]
reps_forced = params["repetitions_forced_choice"]
colours = params["forced_grasp_colours"]
scale_q = params["scale_question"]


sub_info = {
    "ID (sub-00x)": "sub-000",
    "gender (m/f/o)": "o",
    "age": "69"
}

subject = sub_info["ID (sub-00x)"]
gender = sub_info["gender (m/f/o)"]
age = int(sub_info["age"])

prompt = gui.DlgFromDict(
    dictionary=sub_info, 
    title="SUBJECT INFO"
)

timestamp = str(datetime.timestamp(datetime.now()))

data_log = {
    "subject_id": [],
    "gender": [],
    "age": [],
    "task_type": [],
    "trial": [],
    "angle": [],
    "colour": []
}


mon = monitors.Monitor("default")
w_px, h_px, w_cm, h_cm, d_cm = [1920, 1080, 52.70, 29.64, 56]
mon.setWidth(w_cm)
mon.setDistance(d_cm)
mon.setSizePix((w_px, h_px))

win = visual.Window(
    [1920, 1080],
    units="deg",
    monitor=mon,
    color="#000000",
    fullscr=True,
    allowGUI=False,
    winType="pyglet"
)

win.mouseVisible = False

text_stim = visual.TextStim(
    win,
    text="",
    height=0.5,
    color="white",
    pos=(0, 0),
    anchorHoriz="center", 
    anchorVert="center"
)

text_scale = visual.TextStim(
    win,
    text="",
    height=2.5,
    color="red",
    pos=(0, -5),
    anchorHoriz="center", 
    anchorVert="center"
)

core.wait(1)

text_stim.text = "Free choice (1) or Forced choice (0)"
text_stim.draw()
win.flip()
key_pressed = event.waitKeys(
    maxWait=180,
    keyList=["0", "1"],
    modifiers=False, 
    timeStamped=False
)

trial_type = ""

if "1" in key_pressed:
    trial_type = "free"
    conditions = generate_trials(angles, reps_free, type=trial_type)
    

elif "0" in key_pressed:
    trial_type = "forced"
    conditions = generate_trials(angles, reps_free, type=trial_type)
    
filename = "{}_grasp-{}_{}.csv".format(
    subject,
    trial_type,
    timestamp
)

text_stim.text = "Continue (c) or quit (z)?"
text_stim.draw()
win.flip()
key_pressed = event.waitKeys(
    maxWait=180,
    keyList=["c", "q"],
    modifiers=False, 
    timeStamped=False
)
if "y" in key_pressed:
    pass

elif "q" in key_pressed:
    win.close()
    core.quit()

for trial, i in enumerate(conditions):
    colour = ""
    angle = ""
    orientation = ""
    if trial_type == "free":
        angle = i
    if trial_type == "forced":
        angle = int(i[0])
        ori_ix = int(i[1])
        orientation = "Ask participant to put thumb on sticker with {} colour".format(colours[ori_ix])
        colour = colours[ori_ix]

    text_stim.text = "Set angle to {} degrees \n\n {} \n\n Press (g) if participant grasped the object".format(angle, orientation)
    text_stim.draw()
    win.flip()
    event.waitKeys(
        maxWait=180,
        keyList=["g"],
        modifiers=False, 
        timeStamped=False
    )

    if trial_type == "free":
        text_stim.text = "Thumb landed on: \n(1) {} \n (2) {}".format(*colours)
        text_stim.draw()
        win.flip()
        key_pressed = event.waitKeys(
            maxWait=999,
            keyList=["1", "2"],
            modifiers=False, 
            timeStamped=False
        )

        colour = colours[int(key_pressed[0])-1]

    current_key = "waiting for response"
    response = False
    event.clearEvents()
    while True:
        key_pressed = event.getKeys(
            keyList=["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "c", "z"],
            modifiers=False, 
            timeStamped=False
        )

        if len(key_pressed) > 0:
            response = True
            current_key = key_pressed[0]
            if current_key == "0":
                current_key = 10

     
        text_stim.text = "{}\n\nPress (c) to validate the choice\nand continue to next trial \nor\n\n press (z) to quit".format(scale_q)
        text_stim.draw()
        text_scale.text = current_key
        text_scale.draw()
        win.flip()

        if "c" in key_pressed and response:
            break

        elif "z" in key_pressed:
            win.close()
            core.quit()

    data_log["subject_id"].append(subject)
    data_log["gender"].append(gender)
    data_log["age"].append(age)
    data_log["task_type"].append(trial_type)
    data_log["trial"].append(trial)
    data_log["angle"].append(angle)
    data_log["colour"].append(colour)

    pd.DataFrame.from_dict(data_log).to_csv(filename, index=False)

    



print(key_pressed)

win.close()
core.quit()