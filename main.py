import pyttsx3
import logging
import solutions as sol
import helpline
from tkinter import messagebox
import tkinter as tk
from datetime import datetime
import os
import pyttsx3

nat_dis = ['E : Earthquake', 'F : Flood',
           'L : Landslide', 'E : Errosion', 'U : Unemployment']


# GUI
tk.Tk().withdraw()
messagebox.showinfo('Welcome', 'Welcome to the Disaster Management System')


# ------------saving logs--------------------------------------------------------
def initiate_logs():
    logging.info('-------------------------------------'*4)
    logging.info('Log at {}'.format(datetime.now()))


# os.makedirs('logs\log_'+str(datetime.now())+'.log',exist_ok=True)

# logging.basicConfig(
#     filename='logs\log_'+str(datetime.now())+'.log',
#     filemode='w',
#     format='%(name)s - %(levelname)s - %(message)s - %(asctime)s',
#     datefmt='%d-%b-%y %H:%M:%S',
#     level=logging.DEBUG
# )


def save_logs(text, type):
    if type == 'error':
        logging.error(text)
    elif type == 'warning':
        logging.warning(text)
    elif type == 'info':
        logging.info(text)
    elif type == 'debug':
        logging.debug(text)
    elif type == 'critical':
        logging.critical(text)
    elif type == 'exception':
        logging.exception(text)
    else:
        logging.warning('No such log type exists, log is : ' + text)

# ------------------------------------------------------------------------------


# -----------------------------------------initialize the engine--------------------------------------------
engine = pyttsx3.init()     # initialise the engine

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)   # set the voice

newVoiceRate = 140
engine.setProperty('rate', newVoiceRate)    # set the speed rate

# text to speech
def speak(text):
    # save_logs('Jarvis : {}'.format(text), 'info')
    engine.say(text)
    engine.runAndWait()

#-------------------------------------------------------------------------------------------------------

def print_results(inp):
    for i in range(1, 3):
        print(inp[i])
        speak(text=inp[i])
    user_inp = input('Do you want to see more? (y/n) : ')
    if user_inp == 'y':
        for j in range(3, len(inp)+1):
            print(inp[j])
            speak(text=inp[j])


for i in nat_dis:
    print(i)

user_inp = (input('Choose what happened with you? (enter initials): ')).upper()
helpline.helpline_number_acc_to_state()

if user_inp == 'E':
    print_results(sol.earthquake())
elif user_inp == 'F':
    print_results(sol.flood())
elif user_inp == 'L':
    print_results(sol.landside())
elif user_inp == 'U':
    print_results(sol.unemployment())

else:
    print('Invalid input')


print('\n Hold tight, we will provide help ASAP')