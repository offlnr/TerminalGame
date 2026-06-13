# -*- coding: utf-8 -*-
import sys
import random

try:
    import msvcrt
    _HAS_MSVCRT = True
except ImportError:
    _HAS_MSVCRT = False

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from colorama import init as _ci, Fore as _F, Style as _S
_ci(autoreset=True)


class C:
    BLACK   = _F.BLACK;   RED   = _F.RED;   GREEN   = _F.GREEN
    YELLOW  = _F.YELLOW;  BLUE  = _F.BLUE;  MAGENTA = _F.MAGENTA
    CYAN    = _F.CYAN;    WHITE = _F.WHITE
    LGRAY   = _F.LIGHTBLACK_EX
    LRED    = _F.LIGHTRED_EX;   LGREEN  = _F.LIGHTGREEN_EX
    LYELLOW = _F.LIGHTYELLOW_EX; LMAGENTA = _F.LIGHTMAGENTA_EX
    LCYAN   = _F.LIGHTCYAN_EX;  LWHITE  = _F.LIGHTWHITE_EX
    BRIGHT  = _S.BRIGHT;  DIM = _S.DIM;  RESET = _S.RESET_ALL
