import atexit
import os
import readline

from tbvaccine import TBVaccine
from termcolor import colored

from . import evaluate

histfile = os.path.join(os.path.expanduser("~"), ".piems-history")
histfile_size = 1000
readline.set_history_length(1000)

if os.path.exists(histfile):
    readline.read_history_file(histfile)

atexit.register(readline.write_history_file, histfile)

while True:
    try:
        line = input('\001' + colored('\002🐕 \001', 'blue') + '\002')
    except KeyboardInterrupt:
        print()
        break

    try:
        print(evaluate.evaluate(line))
    except Exception as e:
        print(TBVaccine().format_exc())
