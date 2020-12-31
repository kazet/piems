import os
from decimal import InvalidOperation

import readline

from lark.exceptions import UnexpectedEOF, UnexpectedCharacters
from tbvaccine import TBVaccine

from . import evaluate

histfile = os.path.join(os.path.expanduser("~"), ".piems-history")
readline.set_history_length(1000)

if os.path.exists(histfile):
    readline.read_history_file(histfile)


while True:
    try:
        line = input('🐕 ')
    except (KeyboardInterrupt, EOFError):
        print()
        break

    try:
        print(evaluate.evaluate(line))
    except InvalidOperation:
        print("Invalid number operation - are the numbers too big?")
    except (UnexpectedEOF, UnexpectedCharacters) as e:
        print(str(e))
    except Exception:
        print(TBVaccine().format_exc())

    readline.write_history_file(histfile)
