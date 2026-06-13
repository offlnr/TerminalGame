# -*- coding: utf-8 -*-
import sys
import re
import time
import subprocess

from colors import C

W = 70


def clear_screen():
    subprocess.run('cls' if sys.platform == 'win32' else 'clear', shell=True)


def pause(s: float = 1.5):
    time.sleep(s)


def slow_print(text: str, delay: float = 0.03):
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(delay)
    print()


def _visible_len(s: str) -> int:
    return len(re.compile(r'\x1b\[[0-9;]*m').sub('', s))


def box_top(title: str = ''):
    if title:
        t = f'  {title}  '
        left  = (W - len(t)) // 2
        right = W - len(t) - left
        print('╔' + '═' * left + C.BRIGHT + t + C.RESET + '═' * right + '╗')
    else:
        print('╔' + '═' * W + '╗')


def box_div(char: str = '╠', end_char: str = '╣'):
    print(char + '═' * W + end_char)


def box_bot():
    print('╚' + '═' * W + '╝')


def box_row(content: str = '', color: str = ''):
    visible = _visible_len(content)
    pad     = W - visible
    print('║' + color + content + C.RESET + ' ' * max(0, pad) + '║')


def hp_bar(current: int, maximum: int, length: int = 20) -> str:
    if maximum <= 0:
        return '█' * length
    filled = max(0, min(length, int((current / maximum) * length)))
    return C.LRED + '█' * filled + C.LGRAY + '░' * (length - filled) + C.RESET


def mp_bar(current: int, maximum: int, length: int = 20) -> str:
    if maximum <= 0:
        return '█' * length
    filled = max(0, min(length, int((current / maximum) * length)))
    return C.LCYAN + '█' * filled + C.LGRAY + '░' * (length - filled) + C.RESET


def xp_bar(current: int, maximum: int, length: int = 14) -> str:
    if maximum <= 0:
        return '░' * length
    filled = max(0, min(length, int((current / maximum) * length)))
    return C.LGREEN + '█' * filled + C.LGRAY + '░' * (length - filled) + C.RESET


def stamina_pips(current: int, maximum: int) -> str:
    return C.YELLOW + '●' * current + C.LGRAY + '○' * (maximum - current) + C.RESET


def _draw_side_panel(sprite_lines: list, stat_lines: list):
    n = max(len(sprite_lines), len(stat_lines))
    for i in range(n):
        sp = sprite_lines[i] if i < len(sprite_lines) else '    ' + ' ' * 28
        st = stat_lines[i]   if i < len(stat_lines)   else ''
        sp_vis = _visible_len(sp)
        st_vis = _visible_len(st)
        pad    = W - sp_vis - 2 - st_vis
        print('║' + sp + '  ' + st + C.RESET + ' ' * max(0, pad) + '║')
