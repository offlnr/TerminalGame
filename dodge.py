# -*- coding: utf-8 -*-
import sys
import time
import random

try:
    import msvcrt
    _HAS_MSVCRT = True
except ImportError:
    _HAS_MSVCRT = False

from ui import clear_screen

# Dimensiones de la caja de esquiva
_DW = 30   # ancho interior
_DH = 9    # alto interior
_DR = 7    # fila del borde superior (1-indexed, terminal)
_DC = 5    # columna del borde izquierdo (1-indexed, terminal)

# Constantes ANSI sin colorama (para uso dentro del dodge loop)
_RED    = '\x1b[91m'
_YELLOW = '\x1b[93m'
_CYAN   = '\x1b[96m'
_GREEN  = '\x1b[92m'
_DIM    = '\x1b[2m'
_BOLD   = '\x1b[1m'
_RST    = '\x1b[0m'


class Projectile:
    def __init__(self, x: float, y: float, vx: float, vy: float,
                 char: str = '*', homing: float = 0.0):
        self.x      = x
        self.y      = y
        self.vx     = vx
        self.vy     = vy
        self.char   = char
        self.alive  = True
        self.homing = homing
        self._spd   = max(0.1, (vx * vx + vy * vy) ** 0.5)

    def update(self, dt: float, sx: float = None, sy: float = None):
        if self.homing > 0 and sx is not None:
            dx   = sx - self.x
            dy   = sy - self.y
            dist = max(0.1, (dx * dx + dy * dy) ** 0.5)
            t     = min(1.0, self.homing * dt)
            tvx   = (dx / dist) * self._spd
            tvy   = (dy / dist) * self._spd
            self.vx = self.vx * (1 - t) + tvx * t
            self.vy = self.vy * (1 - t) + tvy * t
            spd = max(0.1, (self.vx * self.vx + self.vy * self.vy) ** 0.5)
            self.vx = self.vx / spd * self._spd
            self.vy = self.vy / spd * self._spd
        self.x += self.vx * dt
        self.y += self.vy * dt
        if not (0 <= self.x < _DW and 0 <= self.y < _DH):
            self.alive = False

    @property
    def ix(self): return int(round(self.x))
    @property
    def iy(self): return int(round(self.y))


def _goto(row: int, col: int):
    sys.stdout.write(f'\x1b[{row};{col}H')


def _hide_cursor():
    sys.stdout.write('\x1b[?25l')
    sys.stdout.flush()


def _show_cursor():
    sys.stdout.write('\x1b[?25h')
    sys.stdout.flush()


def _get_key():
    if not _HAS_MSVCRT:
        return None
    if not msvcrt.kbhit():
        return None
    ch = msvcrt.getch()
    if ch in (b'\xe0', b'\x00'):
        ch2 = msvcrt.getch()
        return {b'H': 'UP', b'P': 'DOWN', b'K': 'LEFT', b'M': 'RIGHT'}.get(ch2)
    c = ch.decode('utf-8', errors='ignore').lower()
    return {'w': 'UP', 's': 'DOWN', 'a': 'LEFT', 'd': 'RIGHT'}.get(c)


def _spawn_projectiles(sprite_key: str, elapsed: float, duration: float) -> list:
    phase = elapsed / max(duration, 0.01)
    projs = []

    if sprite_key == "slime":
        for _ in range(2 if phase > 0.5 else 1):
            x = random.randint(1, _DW - 2)
            projs.append(Projectile(x, 0, 0, 2.8 + phase * 0.8, 'o', homing=0.0))

    elif sprite_key == "goblin":
        for _ in range(2 if phase > 0.6 else 1):
            y = random.randint(0, _DH - 1)
            projs.append(Projectile(_DW - 1, y, -(11 + phase * 3), 0, '>', homing=1.5))

    elif sprite_key == "wolf":
        projs.append(Projectile(_DW - 1, 0, -(8 + phase * 2),
                                3.5 + random.uniform(-0.5, 0.5), '*', homing=1.0))
        if phase > 0.5:
            projs.append(Projectile(0, 0, 8 + phase * 2,
                                    3.5 + random.uniform(-0.5, 0.5), '*', homing=1.0))

    elif sprite_key == "skeleton":
        y = random.randint(0, _DH - 1)
        projs.append(Projectile(0,      y,  10.0, 0, '-', homing=0.8))
        projs.append(Projectile(_DW-1,  y, -10.0, 0, '-', homing=0.8))

    elif sprite_key == "orc":
        y = random.randint(1, _DH - 2)
        for dy in (-1, 0, 1):
            ny = y + dy
            if 0 <= ny < _DH:
                projs.append(Projectile(_DW - 1, ny, -(5.0 + phase), 0, '#', homing=0.0))

    elif sprite_key == "dark_mage":
        y  = random.randint(1, _DH - 2)
        vy = random.uniform(-2.0, 2.0)
        projs.append(Projectile(_DW - 1, y,       -9.0, vy,  '@', homing=2.0))
        projs.append(Projectile(_DW - 1, _DH-1-y, -8.5, -vy, '@', homing=2.0))
        if phase > 0.5:
            projs.append(Projectile(0, random.randint(0, _DH-1), 9.0, 0, '@', homing=2.0))

    elif sprite_key == "troll":
        for _ in range(3 if phase > 0.6 else 2 if phase > 0.3 else 1):
            x = random.randint(1, _DW - 2)
            projs.append(Projectile(x, 0, random.uniform(-0.8, 0.8),
                                    2.2 + phase * 0.5, 'O', homing=0.5))

    elif sprite_key == "vampire":
        for _ in range(2 if phase > 0.4 else 1):
            side = random.choice(['L', 'R', 'T', 'B'])
            if side == 'L':   p = Projectile(0,      random.randint(0, _DH-1),  9.0,  0, 'v', homing=3.5)
            elif side == 'R': p = Projectile(_DW-1,  random.randint(0, _DH-1), -9.0,  0, 'v', homing=3.5)
            elif side == 'T': p = Projectile(random.randint(0, _DW-1), 0,        0,   8.0, 'v', homing=3.5)
            else:             p = Projectile(random.randint(0, _DW-1), _DH-1,    0,  -8.0, 'v', homing=3.5)
            projs.append(p)

    elif sprite_key == "demon":
        sp = 11.0 + phase * 3
        for side in random.sample(range(4), 2 if phase < 0.5 else 4):
            if side == 0:   projs.append(Projectile(random.randint(0, _DW-1), 0,    0,  sp, 'V', homing=2.5))
            elif side == 1: projs.append(Projectile(random.randint(0, _DW-1), _DH-1, 0, -sp, '^', homing=2.5))
            elif side == 2: projs.append(Projectile(0, random.randint(0, _DH-1),   sp,  0, '>', homing=2.5))
            else:           projs.append(Projectile(_DW-1, random.randint(0, _DH-1), -sp, 0, '<', homing=2.5))

    elif sprite_key == "dragon":
        gap = random.randint(3, _DW - 4)
        spd = 5.5 + phase * 2.5
        for x in range(_DW):
            if abs(x - gap) > 1:
                projs.append(Projectile(x, 0, 0, spd, '█', homing=0.8))

    return projs


def _spawn_interval(sprite_key: str) -> float:
    return {
        "slime":     0.42,
        "goblin":    0.26,
        "wolf":      0.30,
        "skeleton":  0.34,
        "orc":       0.52,
        "dark_mage": 0.22,
        "troll":     0.38,
        "vampire":   0.26,
        "demon":     0.18,
        "dragon":    0.65,
    }.get(sprite_key, 0.32)


def _dodge_duration(sprite_key: str) -> float:
    return 14.0 if sprite_key == "dragon" else 9.0


def _draw_dodge_static(enemy_name: str):
    clear_screen()
    _goto(1, _DC)
    sys.stdout.write(_RED + _BOLD + f'*** ATAQUE DE {enemy_name.upper()[:30]} ***' + _RST)
    _goto(2, _DC)
    sys.stdout.write(_CYAN + 'Tiempo:' + _RST)
    _goto(3, _DC)
    sys.stdout.write(_GREEN + 'HP:    ' + _RST)
    _goto(5, _DC)
    sys.stdout.write(_DIM + 'Mueve: W A S D  o  flechas del teclado' + _RST)
    _goto(6, _DC)
    sys.stdout.write(_DIM + 'Esquiva todos los proyectiles!' + _RST)
    _goto(_DR, _DC)
    sys.stdout.write('┌' + '─' * _DW + '┐')
    for r in range(_DH):
        _goto(_DR + 1 + r, _DC)
        sys.stdout.write('│' + ' ' * _DW + '│')
    _goto(_DR + 1 + _DH, _DC)
    sys.stdout.write('└' + '─' * _DW + '┘')
    sys.stdout.flush()


def _render_dodge_frame(sx: int, sy: int, projs: list,
                        timer_pct: float, player_hp: int, player_max_hp: int,
                        hits: int):
    t_filled = int(timer_pct * _DW)
    timer_bar = _RED + '█' * t_filled + '\x1b[90m' + '░' * (_DW - t_filled) + _RST
    _goto(2, _DC + 8)
    sys.stdout.write(timer_bar + ' ')

    pct    = player_hp / max(player_max_hp, 1)
    h_fill = int(pct * 20)
    hp_bar_str = _RED + '█' * h_fill + '\x1b[90m' + '░' * (20 - h_fill) + _RST
    _goto(3, _DC + 8)
    sys.stdout.write(hp_bar_str + f' {player_hp}/{player_max_hp}   ')

    for row in range(_DH):
        _goto(_DR + 1 + row, _DC + 1)
        chars = [(' ', 0)] * _DW
        for p in projs:
            if p.iy == row and 0 <= p.ix < _DW:
                chars[p.ix] = (p.char, 1)
        if sy == row and 0 <= sx < _DW:
            chars[sx] = ('♥', 2)
        line = ''
        for ch, kind in chars:
            if kind == 2:
                line += _RED + _BOLD + '♥' + _RST
            elif kind == 1:
                line += _YELLOW + ch + _RST
            else:
                line += ch
        sys.stdout.write(line)

    _goto(_DR + _DH + 2, _DC)
    if hits == 0:
        sys.stdout.write(_GREEN + 'Sin golpes!           ' + _RST)
    else:
        sys.stdout.write(_RED + f'Golpes recibidos: {hits}' + _RST + '   ')

    sys.stdout.flush()


def run_dodge_phase(enemy, player) -> int:
    sx, sy  = _DW // 2, _DH // 2
    projs   = []
    hits    = 0
    dmg     = 0
    iframes = 0.0

    duration = _dodge_duration(enemy.sprite_key)
    interval = _spawn_interval(enemy.sprite_key)
    hit_dmg  = max(8, enemy.attack // 3)

    _hide_cursor()
    _draw_dodge_static(enemy.name)

    start      = time.time()
    last_frame = start
    last_spawn = start - interval

    try:
        while True:
            now     = time.time()
            elapsed = now - start
            dt      = now - last_frame
            last_frame = now

            if elapsed >= duration:
                break

            key = _get_key()
            if   key == 'UP'    and sy > 0:        sy -= 1
            elif key == 'DOWN'  and sy < _DH - 1:  sy += 1
            elif key == 'LEFT'  and sx > 0:         sx -= 1
            elif key == 'RIGHT' and sx < _DW - 1:  sx += 1

            if now - last_spawn >= interval:
                last_spawn = now
                projs.extend(_spawn_projectiles(enemy.sprite_key, elapsed, duration))

            for p in projs:
                p.update(dt, float(sx), float(sy))
            projs = [p for p in projs if p.alive]

            if iframes <= 0:
                for p in projs:
                    if p.ix == sx and p.iy == sy:
                        hits    += 1
                        dmg     += hit_dmg
                        iframes  = 0.45
                        p.alive  = False
                        break
            else:
                iframes -= dt
            projs = [p for p in projs if p.alive]

            timer_pct = max(0.0, 1.0 - elapsed / duration)
            _render_dodge_frame(sx, sy, projs, timer_pct,
                                player.hp, player.max_hp, hits)

            time.sleep(0.045)

    finally:
        _show_cursor()

    _goto(_DR + _DH + 4, _DC)
    if dmg == 0:
        sys.stdout.write(_GREEN + _BOLD + '*** PERFECTO! Sin dano recibido! ***' + _RST + '   ')
    else:
        sys.stdout.write(_RED + f'*** -{dmg} HP de dano recibido ***' + _RST + '   ')
    sys.stdout.flush()
    time.sleep(1.5)

    return dmg
