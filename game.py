# -*- coding: utf-8 -*-
"""
TERMINAL RPG  -  Undertale Combat Edition
Requiere: pip install colorama
"""

import sys
import time
import random
import subprocess

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


# ═══════════════════════════════════════════════════════
#  MOTOR DE PIXEL ART
# ═══════════════════════════════════════════════════════

_PALETTE = {
    '.': ('',                   '  '),
    'K': (C.LGRAY,              '██'),
    'W': (C.LWHITE,             '██'),
    'w': (C.WHITE,              '██'),
    'R': (C.RED,                '██'),
    'r': (C.LRED,               '██'),
    'G': (C.GREEN,              '██'),
    'g': (C.LGREEN,             '██'),
    'Y': (C.YELLOW,             '██'),
    'y': (C.LYELLOW,            '██'),
    'B': (C.BLUE,               '██'),
    'M': (C.MAGENTA,            '██'),
    'm': (C.LMAGENTA,           '██'),
    'C': (C.CYAN,               '██'),
    'c': (C.LCYAN,              '██'),
    'S': (C.LGRAY,              '▓▓'),
    'O': (C.LYELLOW,            '▓▓'),
    'D': (C.YELLOW,             '▓▓'),
    'P': (C.LMAGENTA,           '▓▓'),
    'N': (C.BLACK + C.BRIGHT,   '░░'),
}

def _px(row: str) -> str:
    out = ''
    for code in row:
        color, block = _PALETTE.get(code, ('', '  '))
        out += (color + block + C.RESET) if color else block
    return out

ENEMY_SPRITES = {
    "slime": [
        "....ccCCCCcc....",
        "..ccCCCCCCCCcc..",
        ".cCCCCCCCCCCCCc.",
        ".cCCcWwcccWwcCCc",
        ".cCCcccCCCcccCCc",
        ".cCCCCCCCCCCCCc.",
        "..ccCCCCCCCCcc..",
        "....cccccccc....",
    ],
    "goblin": [
        ".....GgGGGGgG.....",
        "...GGGGGGGGGGGg...",
        "..GGGgGGGGGGgGGG..",
        ".GGGGWwGGGGGWwGGGG",
        ".GGGGGGgGGGgGGGGGG",
        ".GGGGYyYyYyYyGGGGG",
        ".GGGGGGGGGGGGGGGGg",
        "..DDDDDDDDDDDDDDDD",
        "..DdDDddddddDDdD..",
        "....DD......DD....",
    ],
    "wolf": [
        "..yYY......yYY....",
        ".yYYYy....yYYYy...",
        "yYYYYYyyyyYYYYYy..",
        "yYYYYYYYYYYYYYYYy.",
        "yYYYWwYYYYYWwYYYy.",
        ".yYYYYyYYyYYYYYy..",
        ".yYYYYYYYYYYYYYy..",
        "..yYYYYYYYYYYYy...",
        "..YyYY.....YyYY...",
        "...yY.......yY....",
    ],
    "skeleton": [
        "....wwWWWWww......",
        "...wWWWWWWWWw.....",
        "..wWWwWWWWwWWw....",
        "..wWWKkWWWKkWWw...",
        "..wWWWWwwwWWWWw...",
        "..wWWWWWWWWWWWw...",
        "...SSSSSSSSSSSS...",
        "...SsSsSsSsSsSs...",
        "...SS.......SS....",
        "...SS.......SS....",
    ],
    "orc": [
        "...GGGGGGGGGGg....",
        "..GGGGGGGGGGGGg...",
        ".GGGRrGGGGGRrGGG..",
        ".GGGGGGgGgGGGGGGG.",
        ".GGGGGGGGGGGGGGGg.",
        ".SSSSSSSSSSSSSSSS.",
        ".SSSSSSsSSsSSSSSSS",
        ".SSSSS.....SSSSSSS",
        "..KKK.......KKK...",
        "..KK.........KK...",
    ],
    "dark_mage": [
        ".....mMMMMMMm.....",
        "....mMMMMMMMMMm...",
        "...mMMwWMMMWwMMm..",
        "...mMMMMMMMMMMMm..",
        "...mMMMmMMmMMMm...",
        "..MMMMMMMMMMMMMMm.",
        ".MMMmMMMMMMMmMMMM.",
        ".MMMMMmMMMmMMMMM..",
        "..MMMMMmMmMMMMM...",
        "....mmMMMMMmm.....",
    ],
    "troll": [
        ".SSSSSSSSSSSSSSSSS",
        "SSSSSSSSSSSSSSSSSSs",
        "SSSSwWSSSSSSwWSSSSS",
        "SSSSSSSSsSSSSSSSSSS",
        "SSSSSSSSSSSSSSSSSSs",
        "SSSSKkSSSSSSKkSSSSS",
        "SSSSSSSSSSSSSSSSSSs",
        "SSSSSSSSSSSSSSSSSSS",
        ".SSSSSS.....SSSSSSs",
        "..SSSS.......SSSS..",
    ],
    "vampire": [
        "....MMMMMMMM......",
        "...MMMMMMMMMMm....",
        "..MMmWwMMMWwMMMm..",
        "..MMMMMMmMMMMMMM..",
        "..MMMMMMMMMMMMmM..",
        "..RRRMMMMMMMMrr...",
        ".RRRRRRRRRRRRRRr..",
        "..MMMRRRRRRRMMm...",
        "....MM......MM....",
        "....MM......MM....",
    ],
    "demon": [
        "R...RRRRRRRR...R..",
        "RR..RRRrRRRR..RR..",
        ".RRRRRRRRRRRRRRr..",
        ".RRRyYRRRRRyYRRR..",
        ".RRRRRRrRRRRRRRR..",
        ".RRRRRRRRRRRRRRr..",
        "..RRRRRRRRRRRRR...",
        "..RR.RRRRRRR.RR...",
        "R....RRRRRRR....R.",
        "RR...........RR...",
    ],
    "dragon": [
        "RR..............RR",
        "RRRr..........rRRR",
        "RRRRRr......rRRRRR",
        ".RRRRRRrrrrRRRRRR.",
        ".RRRRyYRRRRyYRRRR.",
        "..RRRRRRrRRRRRRR..",
        "..RRRRRRRRRRRRrr..",
        "...rRRRRRRRRRRr...",
        "..rRRR......RRRr..",
        ".rRRR........RRRr.",
        "rRRR..........RRRr",
        ".RRR..........RRR.",
    ],
}

PLAYER_SPRITES = {
    "Guerrero": [
        "....YYYYY.....",
        "...YYYyyYYY...",
        "..YYwWYYwWYY..",
        "..YYYYYYYYYy..",
        "..SSSSSSSSSS..",
        ".SSSSyyySSSSSS",
        ".SSSSyyySSSSSSS",
        "..KKKK.KKKK...",
        "..KKK...KKK...",
        "..KK.....KK...",
    ],
    "Mago": [
        "....MMMMM.....",
        "...MMMmMMMM...",
        "..MMwWMMwWMM..",
        "...MMMMMMMMM..",
        "...mMMMMMMmm..",
        "..MMMMMMMMMMm.",
        ".MMMmMMMmMMMM.",
        "..MmMMMMMMmM..",
        "....MM..MM....",
        "....mm..mm....",
    ],
}

def render_sprite(rows: list, indent: int = 4) -> list:
    pad = ' ' * indent
    return [pad + _px(row) for row in rows]


# ═══════════════════════════════════════════════════════
#  INTERFAZ CON MARCOS
# ═══════════════════════════════════════════════════════

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

def _visible_len(s: str) -> int:
    import re
    return len(re.compile(r'\x1b\[[0-9;]*m').sub('', s))

def hp_bar(current: int, maximum: int, length: int = 20) -> str:
    if maximum <= 0:
        return '█' * length
    pct    = current / maximum
    filled = max(0, min(length, int(pct * length)))
    color  = C.GREEN if pct > 0.5 else (C.YELLOW if pct > 0.25 else C.RED)
    return color + '█' * filled + C.LGRAY + '░' * (length - filled) + C.RESET

def xp_bar(current: int, maximum: int, length: int = 14) -> str:
    if maximum <= 0:
        return '░' * length
    filled = max(0, min(length, int((current / maximum) * length)))
    return C.CYAN + '█' * filled + C.LGRAY + '░' * (length - filled) + C.RESET

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


# ═══════════════════════════════════════════════════════
#  PERSONAJES
# ═══════════════════════════════════════════════════════

class Character:
    def __init__(self, name, hp, attack, magic_power, defense):
        self.name        = name
        self.max_hp      = hp
        self.hp          = hp
        self.attack      = attack
        self.magic_power = magic_power
        self.defense     = defense
        self.level       = 1
        self.xp          = 0
        self.xp_to_next  = 100
        self.potions     = 2
        self.gold        = 0

    @property
    def is_alive(self): return self.hp > 0

    def take_damage(self, raw: int) -> int:
        reduced = max(1, raw - self.defense // 2)
        self.hp = max(0, self.hp - reduced)
        return reduced

    def heal(self, amount: int):
        self.hp = min(self.max_hp, self.hp + amount)

    def use_potion(self) -> tuple:
        if self.potions <= 0:
            return False, 'No tienes pociones.'
        self.potions -= 1
        amt = int(self.max_hp * 0.45)
        self.heal(amt)
        return True, f'Usas una Pocion. +{amt} HP.'

    def physical_attack(self, target) -> int:
        raw = int(self.attack * random.uniform(0.80, 1.20))
        return target.take_damage(raw)

    def gain_xp(self, amount: int) -> bool:
        self.xp += amount
        leveled = False
        while self.xp >= self.xp_to_next:
            self.xp       -= self.xp_to_next
            self.xp_to_next = int(self.xp_to_next * 1.5)
            self._level_up_bonuses()
            self.level    += 1
            self.hp        = self.max_hp
            leveled        = True
        return leveled

    def _level_up_bonuses(self):
        self.max_hp  += 10
        self.attack  += 2
        self.defense += 1


class Warrior(Character):
    CLASS_NAME = "Guerrero"
    SPRITE_KEY = "Guerrero"
    COLOR      = C.YELLOW

    def __init__(self, name):
        super().__init__(name, hp=140, attack=22, magic_power=0, defense=12)
        self.max_stamina = 3
        self.stamina     = 3

    def _level_up_bonuses(self):
        self.max_hp      += 22
        self.attack      += 5
        self.defense     += 3
        self.max_stamina  = min(self.max_stamina + 1, 6)
        self.stamina      = self.max_stamina

    def power_strike(self, target) -> tuple:
        if self.stamina <= 0:
            return None, 'Sin Stamina.'
        self.stamina -= 1
        raw    = int(self.attack * 2.2 * random.uniform(0.90, 1.30))
        dmg    = target.take_damage(raw)
        return dmg, f'GOLPE DEVASTADOR! {dmg} dano.'

    def war_cry(self) -> tuple:
        if self.stamina < 2:
            return None, 'Necesitas 2 Stamina.'
        self.stamina -= 2
        bonus = int(self.attack * 0.5)
        self.attack += bonus
        return bonus, f'GRITO DE GUERRA! ATK +{bonus}.'

    def draw_status_row(self):
        stm = stamina_pips(self.stamina, self.max_stamina)
        pot = f'{C.GREEN}[P:{self.potions}]{C.RESET}'
        box_row(f'  {C.YELLOW}{C.BRIGHT}{self.CLASS_NAME}: {self.name}{C.RESET}  Nv.{self.level}  '
                f'HP {hp_bar(self.hp, self.max_hp)} {self.hp}/{self.max_hp}  {pot}')
        box_row(f'  STM: {stm}   XP: {xp_bar(self.xp, self.xp_to_next)}')

    def draw_full(self):
        lines = render_sprite(PLAYER_SPRITES[self.SPRITE_KEY])
        stats = [
            f' {C.YELLOW}{C.BRIGHT}{self.CLASS_NAME}: {self.name}{C.RESET}  Nv.{self.level}',
            f' HP  {hp_bar(self.hp, self.max_hp, 16)} {self.hp}/{self.max_hp}',
            f' STM {stamina_pips(self.stamina, self.max_stamina)}',
            f' XP  {xp_bar(self.xp, self.xp_to_next)} {self.xp}/{self.xp_to_next}',
            f' ATK {self.attack}   DEF {self.defense}',
            f' {C.GREEN}Pociones: {self.potions}{C.RESET}   Oro: {self.gold}',
        ]
        _draw_side_panel(lines, stats)


class Mage(Character):
    CLASS_NAME = "Mago"
    SPRITE_KEY = "Mago"
    COLOR      = C.MAGENTA

    SPELLS = {
        1: {"name": "Bola de Fuego",   "cost": 15, "mult": 2.0, "type": "damage", "desc": "Alto dano de fuego"},
        2: {"name": "Rayo de Hielo",   "cost": 10, "mult": 1.4, "type": "damage", "desc": "Bajo costo, buen dano"},
        3: {"name": "Curacion Arcana", "cost": 20, "mult": 1.6, "type": "heal",   "desc": "Restaura HP propio"},
        4: {"name": "Tormenta Arcana", "cost": 30, "mult": 2.8, "type": "damage", "desc": "El hechizo mas potente"},
    }

    def __init__(self, name):
        super().__init__(name, hp=90, attack=9, magic_power=28, defense=4)
        self.max_mana = 75
        self.mana     = 75

    def _level_up_bonuses(self):
        self.max_hp      += 14
        self.magic_power += 6
        self.max_mana    += 18
        self.mana         = min(self.mana + 18, self.max_mana)
        self.defense     += 1

    def cast_spell(self, spell_id: int, target=None) -> tuple:
        spell = self.SPELLS.get(spell_id)
        if not spell: return None, 'Hechizo desconocido.'
        if self.mana < spell["cost"]: return None, f'Mana insuficiente ({spell["cost"]} MP).'
        self.mana -= spell["cost"]
        var = random.uniform(0.85, 1.15)
        if spell["type"] == "damage":
            raw    = int(self.magic_power * spell["mult"] * var)
            effect = target.take_damage(raw)
            msg    = f'{spell["name"]}! {effect} dano magico.'
        else:
            effect = int(self.magic_power * spell["mult"] * var)
            self.heal(effect)
            msg = f'{spell["name"]}! +{effect} HP.'
        return effect, msg

    def restore_mana(self, amount: int):
        self.mana = min(self.max_mana, self.mana + amount)

    def draw_status_row(self):
        pot = f'{C.GREEN}[P:{self.potions}]{C.RESET}'
        box_row(f'  {C.MAGENTA}{C.BRIGHT}{self.CLASS_NAME}: {self.name}{C.RESET}  Nv.{self.level}  '
                f'HP {hp_bar(self.hp, self.max_hp)} {self.hp}/{self.max_hp}  {pot}')
        box_row(f'  MP {hp_bar(self.mana, self.max_mana)} {self.mana}/{self.max_mana}'
                f'   XP {xp_bar(self.xp, self.xp_to_next)}')

    def draw_full(self):
        lines = render_sprite(PLAYER_SPRITES[self.SPRITE_KEY])
        stats = [
            f' {C.MAGENTA}{C.BRIGHT}{self.CLASS_NAME}: {self.name}{C.RESET}  Nv.{self.level}',
            f' HP  {hp_bar(self.hp, self.max_hp, 16)} {self.hp}/{self.max_hp}',
            f' MP  {hp_bar(self.mana, self.max_mana, 16)} {self.mana}/{self.max_mana}',
            f' XP  {xp_bar(self.xp, self.xp_to_next)} {self.xp}/{self.xp_to_next}',
            f' MGK {self.magic_power}   DEF {self.defense}',
            f' {C.GREEN}Pociones: {self.potions}{C.RESET}   Oro: {self.gold}',
        ]
        _draw_side_panel(lines, stats)


# ═══════════════════════════════════════════════════════
#  ENEMIGOS
# ═══════════════════════════════════════════════════════

class Enemy:
    def __init__(self, name, hp, attack, defense, xp_reward, gold, sprite_key, color):
        self.name       = name
        self.max_hp     = hp
        self.hp         = hp
        self.attack     = attack
        self.defense    = defense
        self.xp_reward  = xp_reward
        self.gold       = gold
        self.sprite_key = sprite_key
        self.color      = color

    @property
    def is_alive(self): return self.hp > 0

    def take_damage(self, raw: int) -> int:
        reduced = max(1, raw - self.defense // 2)
        self.hp = max(0, self.hp - reduced)
        return reduced

    def draw(self):
        rows  = ENEMY_SPRITES.get(self.sprite_key, [])
        lines = render_sprite(rows, indent=4)
        bar   = hp_bar(self.hp, self.max_hp, 18)
        stats = [
            f' {self.color}{C.BRIGHT}{self.name}{C.RESET}',
            f' HP  {bar} {self.hp}/{self.max_hp}',
            f' ATK {C.YELLOW}{self.attack}{C.RESET}   DEF {self.defense}',
        ]
        _draw_side_panel(lines, stats)


_TEMPLATES = {
    "slime":     ("Slime",         40,  7,  1,  45,  4, "slime",     C.CYAN),
    "goblin":    ("Goblin",        50, 10,  2,  60,  6, "goblin",    C.GREEN),
    "wolf":      ("Lobo Feroz",    60, 16,  3,  70,  8, "wolf",      C.YELLOW),
    "skeleton":  ("Esqueleto",     70, 14,  6,  80,  9, "skeleton",  C.WHITE),
    "orc":       ("Orco Guerrero", 105, 23, 10, 110, 16, "orc",      C.LGREEN),
    "dark_mage": ("Mago Oscuro",   80, 25,  5, 130, 20, "dark_mage", C.MAGENTA),
    "troll":     ("Troll de Roca", 125, 21, 13, 150, 24, "troll",    C.LGRAY),
    "vampire":   ("Vampiro",       90, 22,  7, 140, 22, "vampire",   C.LMAGENTA),
    "demon":     ("Demonio Mayor", 110, 28,  8, 160, 28, "demon",    C.RED),
}

def get_act_enemy(act: int) -> Enemy:
    pools = {1: ["slime","goblin","wolf"],
             2: ["wolf","skeleton","orc"],
             3: ["dark_mage","troll","vampire","demon"]}
    key = random.choice(pools.get(act, ["goblin"]))
    n, hp, atk, dfn, xp, gold, skey, color = _TEMPLATES[key]
    return Enemy(n, hp, atk, dfn, xp, gold, skey, color)

def get_malachar() -> Enemy:
    return Enemy("Malachar, Senor del Abismo", 250, 40, 16, 600, 999, "dragon", C.RED)


# ── Datos para el sistema ACT ──────────────────────────

# (nombre_accion, texto_resultado, cambio_enojo)
_ENEMY_ACTS = {
    "slime":     [("Observar",   "Es un slime. Burbujea nerviosamente.", -1),
                  ("Saludar",    "El slime vibra... le gustaste un poco.", -2)],
    "goblin":    [("Hablar",     "'Eh? No huyes?' El goblin duda.", -1),
                  ("Intimidar",  "El goblin retrocede. Sus manos tiemblan.", -2)],
    "wolf":      [("Calmarse",   "Te agachas. El lobo baja la guardia.", -1),
                  ("Aullar",     "El lobo ladea la cabeza sorprendido.", -2)],
    "skeleton":  [("Hablar",     "El esqueleto no tiene orejas. Fracaso.", 0),
                  ("Descanso",   "'Descanso?' El esqueleto parece aliviado.", -2)],
    "orc":       [("Retar",      "Al orco le gustas. Atacara mas fuerte.", 0),
                  ("Negociar",   "'Oro por tu vida?' El orco reflexiona.", -2)],
    "dark_mage": [("Debatir",    "El mago oscuro debate filosofia magica.", -1),
                  ("Ignorar",    "Le ignoras. Se enoja aun mas.", 0)],
    "troll":     [("Elogiar",    "'Eres muy... grande.' El troll sonrie.", -1),
                  ("Acertijo",   "Le haces un acertijo. Parpadea confuso.", -1)],
    "vampire":   [("Preguntar",  "'Por que sirves a Malachar?' El vampiro duda.", -1),
                  ("Espejo",     "El vampiro huye del espejo imaginario.", -2)],
    "demon":     [("Gritar",     "Gritas mas fuerte que el demonio. Empate.", 0),
                  ("Rezar",      "El demonio retrocede ante tu fe.", -2)],
    "dragon":    [("Confrontar", "'Yo no te tengo miedo.' Malachar rie.", 0),
                  ("Desafiar",   "Le miras fijo. Sus llamas vacilan un instante.", -1)],
}

_ENEMY_SPARE_LINES = {
    "slime":     "El slime te mira un momento... y se aleja sin darte problemas.",
    "goblin":    "El goblin suelta el arma y corre. 'Sabia decision.'",
    "wolf":      "El lobo te da la espalda y se pierde en el bosque.",
    "skeleton":  "Los huesos caen al suelo. Por fin descansan.",
    "orc":       "El orco te senala con respeto y parte en otra direccion.",
    "dark_mage": "El mago teletransporta en silencio. No regresara.",
    "troll":     "El troll te deja pasar. Gruye algo que suena a 'adios'.",
    "vampire":   "El vampiro se convierte en murcielago y desaparece.",
    "demon":     "El demonio observa tu calma. Se inclina. Y desaparece.",
    "dragon":    "Malachar no puede ser perdonado.",
}


# ═══════════════════════════════════════════════════════
#  SISTEMA DE ESQUIVA EN TIEMPO REAL (UNDERTALE)
# ═══════════════════════════════════════════════════════

# Dimensiones de la caja de esquiva
_DW  = 30   # ancho interior
_DH  = 9    # alto interior
_DR  = 7    # fila del borde superior (1-indexed, terminal)
_DC  = 5    # columna del borde izquierdo (1-indexed, terminal)

# Constantes ANSI sin colorama (para uso dentro del dodge loop)
_RED    = '\x1b[91m'
_YELLOW = '\x1b[93m'
_CYAN   = '\x1b[96m'
_GREEN  = '\x1b[92m'
_DIM    = '\x1b[2m'
_BOLD   = '\x1b[1m'
_RST    = '\x1b[0m'


class Projectile:
    """Un proyectil en la caja de esquiva."""
    def __init__(self, x: float, y: float, vx: float, vy: float, char: str = '*'):
        self.x    = x
        self.y    = y
        self.vx   = vx   # cols por segundo
        self.vy   = vy   # filas por segundo
        self.char = char
        self.alive = True

    def update(self, dt: float):
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
    """Non-blocking key read. Returns 'UP','DOWN','LEFT','RIGHT' or None."""
    if not _HAS_MSVCRT:
        return None
    if not msvcrt.kbhit():
        return None
    ch = msvcrt.getch()
    if ch in (b'\xe0', b'\x00'):
        ch2 = msvcrt.getch()
        return {b'H':'UP', b'P':'DOWN', b'K':'LEFT', b'M':'RIGHT'}.get(ch2)
    c = ch.decode('utf-8', errors='ignore').lower()
    return {'w':'UP','s':'DOWN','a':'LEFT','d':'RIGHT'}.get(c)


def _spawn_projectiles(sprite_key: str, elapsed: float, duration: float) -> list:
    """Devuelve nuevos proyectiles para este frame según el tipo de enemigo."""
    phase = elapsed / max(duration, 0.01)
    projs = []

    if sprite_key == "slime":
        x = random.randint(1, _DW - 2)
        projs.append(Projectile(x, 0, 0, 2.5 + phase, 'o'))

    elif sprite_key == "goblin":
        y = random.randint(0, _DH - 1)
        projs.append(Projectile(_DW - 1, y, -(10 + phase * 4), 0, '>'))

    elif sprite_key == "wolf":
        projs.append(Projectile(_DW - 1, 0, -(7 + phase * 2),
                                3 + random.uniform(-0.5, 0.5), '*'))

    elif sprite_key == "skeleton":
        y = random.randint(0, _DH - 1)
        if random.random() < 0.5:
            projs.append(Projectile(0, y, 9.0, 0, '-'))
        else:
            projs.append(Projectile(_DW - 1, y, -9.0, 0, '-'))

    elif sprite_key == "orc":
        y = random.randint(1, _DH - 2)
        for dy in (-1, 0, 1):
            ny = y + dy
            if 0 <= ny < _DH:
                projs.append(Projectile(_DW - 1, ny, -4.5, 0, '#'))

    elif sprite_key == "dark_mage":
        y = random.randint(1, _DH - 2)
        vy = random.uniform(-2.5, 2.5)
        projs.append(Projectile(_DW - 1, y, -8.0, vy, '@'))
        if phase > 0.4:
            projs.append(Projectile(_DW - 1, _DH - 1 - y, -7.5, -vy, '@'))

    elif sprite_key == "troll":
        x = random.randint(1, _DW - 2)
        projs.append(Projectile(x, 0, random.uniform(-1, 1), 2.0, 'O'))
        if phase > 0.5:
            projs.append(Projectile(random.randint(1, _DW - 2), 0,
                                    random.uniform(-1, 1), 2.3, 'O'))

    elif sprite_key == "vampire":
        side = random.choice(['L', 'R'])
        x0   = 0 if side == 'L' else _DW - 1
        vx0  = 8.0 if side == 'L' else -8.0
        y    = random.randint(0, _DH - 1)
        projs.append(Projectile(x0, y, vx0, random.uniform(-1.5, 1.5), 'v'))

    elif sprite_key == "demon":
        side = random.randint(0, 3)
        sp   = 10.0 + phase * 3
        if side == 0:   projs.append(Projectile(random.randint(0,_DW-1), 0, 0, sp, 'V'))
        elif side == 1: projs.append(Projectile(random.randint(0,_DW-1),_DH-1, 0,-sp, '^'))
        elif side == 2: projs.append(Projectile(0, random.randint(0,_DH-1), sp, 0, '>'))
        else:           projs.append(Projectile(_DW-1,random.randint(0,_DH-1),-sp, 0, '<'))
        if phase > 0.5:
            s2 = (side + 2) % 4
            if s2 == 0:   projs.append(Projectile(random.randint(0,_DW-1), 0, 0, sp, 'V'))
            elif s2 == 1: projs.append(Projectile(random.randint(0,_DW-1),_DH-1, 0,-sp, '^'))
            elif s2 == 2: projs.append(Projectile(0, random.randint(0,_DH-1), sp, 0, '>'))
            else:         projs.append(Projectile(_DW-1,random.randint(0,_DH-1),-sp, 0, '<'))

    elif sprite_key == "dragon":
        # Malachar: pared de fuego con hueco
        gap = random.randint(3, _DW - 4)
        for x in range(_DW):
            if abs(x - gap) > 1:
                projs.append(Projectile(x, 0, 0, 5.0 + phase * 2, '█'))

    return projs


def _spawn_interval(sprite_key: str) -> float:
    return {
        "slime":     0.55,
        "goblin":    0.35,
        "wolf":      0.40,
        "skeleton":  0.45,
        "orc":       0.65,
        "dark_mage": 0.30,
        "troll":     0.50,
        "vampire":   0.38,
        "demon":     0.25,
        "dragon":    0.80,
    }.get(sprite_key, 0.40)


def _dodge_duration(sprite_key: str) -> float:
    return 4.5 if sprite_key == "dragon" else 3.5


def _draw_dodge_static(enemy_name: str):
    """Dibuja el marco estático de la caja de esquiva."""
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
    # Bordes de la caja
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
    """Actualiza solo el contenido dinámico sin redibujar bordes."""
    # Timer
    t_filled = int(timer_pct * _DW)
    timer_bar = _RED + '█' * t_filled + '\x1b[90m' + '░' * (_DW - t_filled) + _RST
    _goto(2, _DC + 8)
    sys.stdout.write(timer_bar + ' ')

    # HP
    pct    = player_hp / max(player_max_hp, 1)
    h_col  = _GREEN if pct > 0.5 else (_YELLOW if pct > 0.25 else _RED)
    h_fill = int(pct * 20)
    hp_bar_str = h_col + '█' * h_fill + '\x1b[90m' + '░' * (20 - h_fill) + _RST
    _goto(3, _DC + 8)
    sys.stdout.write(hp_bar_str + f' {player_hp}/{player_max_hp}   ')

    # Inner rows
    for row in range(_DH):
        _goto(_DR + 1 + row, _DC + 1)
        chars = [(' ', 0)] * _DW   # (char, type 0=empty 1=proj 2=soul)
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

    # Hit counter
    _goto(_DR + _DH + 2, _DC)
    if hits == 0:
        sys.stdout.write(_GREEN + 'Sin golpes!           ' + _RST)
    else:
        sys.stdout.write(_RED + f'Golpes recibidos: {hits}' + _RST + '   ')

    sys.stdout.flush()


def run_dodge_phase(enemy: Enemy, player) -> int:
    """
    Mini-juego de esquiva en tiempo real.
    Devuelve el daño total recibido.
    """
    sx, sy  = _DW // 2, _DH // 2
    projs   = []
    hits    = 0
    dmg     = 0
    iframes = 0.0   # invincibility cooldown after hit

    duration = _dodge_duration(enemy.sprite_key)
    interval = _spawn_interval(enemy.sprite_key)
    hit_dmg  = max(2, enemy.attack // 6)

    _hide_cursor()
    _draw_dodge_static(enemy.name)

    start      = time.time()
    last_frame = start
    last_spawn = start - interval  # spawn immediately

    try:
        while True:
            now     = time.time()
            elapsed = now - start
            dt      = now - last_frame
            last_frame = now

            if elapsed >= duration:
                break

            # Input
            key = _get_key()
            if   key == 'UP'    and sy > 0:        sy -= 1
            elif key == 'DOWN'  and sy < _DH - 1:  sy += 1
            elif key == 'LEFT'  and sx > 0:         sx -= 1
            elif key == 'RIGHT' and sx < _DW - 1:  sx += 1

            # Spawn
            if now - last_spawn >= interval:
                last_spawn = now
                projs.extend(_spawn_projectiles(enemy.sprite_key, elapsed, duration))

            # Update
            for p in projs:
                p.update(dt)
            projs = [p for p in projs if p.alive]

            # Collision (con iframes)
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

            # Render
            timer_pct = max(0.0, 1.0 - elapsed / duration)
            _render_dodge_frame(sx, sy, projs, timer_pct,
                                player.hp, player.max_hp, hits)

            time.sleep(0.045)   # ~22 FPS

    finally:
        _show_cursor()

    # Resultado al salir
    _goto(_DR + _DH + 4, _DC)
    if dmg == 0:
        sys.stdout.write(_GREEN + _BOLD + '*** PERFECTO! Sin dano recibido! ***' + _RST + '   ')
    else:
        sys.stdout.write(_RED + f'*** -{dmg} HP de dano recibido ***' + _RST + '   ')
    sys.stdout.flush()
    time.sleep(1.5)

    return dmg


# ═══════════════════════════════════════════════════════
#  COMBATE ESTILO UNDERTALE
# ═══════════════════════════════════════════════════════

def _draw_ut_header(player, enemy, round_num: int, log: list = None):
    clear_screen()
    box_top(f'  COMBATE  -  Ronda {round_num}  ')
    box_row()
    enemy.draw()
    box_row()
    box_div()
    if log:
        for line in log:
            box_row(f'  {line}')
    else:
        box_row(f'  {C.DIM}Elige tu accion...{C.RESET}')
    box_div()
    player.draw_status_row()
    box_div()


def _fight_menu(player, enemy) -> tuple:
    """Submenu LUCHAR. Retorna (mensaje, acted)."""
    while True:
        clear_screen()
        box_top('  LUCHAR  ')
        box_row()
        box_row(f'  {C.GREEN}[1]{C.RESET} Ataque Fisico')
        if isinstance(player, Mage):
            box_row(f'  {C.MAGENTA}[2]{C.RESET} Lanzar Hechizo')
        else:
            sc = C.GREEN if player.stamina > 0 else C.RED
            wc = C.CYAN  if player.stamina >= 2 else C.RED
            box_row(f'  {C.YELLOW}[2]{C.RESET} Golpe Devastador'
                    f'  (STM: {sc}{player.stamina}/{player.max_stamina}{C.RESET})')
            box_row(f'  {C.CYAN}[3]{C.RESET} Grito de Guerra  '
                    f'(STM: {wc}{player.stamina}/{player.max_stamina}{C.RESET})  ATK+')
        box_row()
        box_row(f'  {C.DIM}[0] Volver{C.RESET}')
        box_bot()
        ch = input('  > ').strip()

        if ch == '0':
            return '', False
        if ch == '1':
            dmg = player.physical_attack(enemy)
            return (f'{C.GREEN}Atacas a {enemy.name}: {C.BRIGHT}{dmg}{C.RESET}'
                    f'{C.GREEN} dano fisico.{C.RESET}'), True
        if ch == '2':
            if isinstance(player, Mage):
                # Spell submenu
                while True:
                    clear_screen()
                    box_top('  GRIMORIO  ')
                    box_row(f'  {C.CYAN}Mana: {player.mana}/{player.max_mana}{C.RESET}')
                    box_div()
                    for sid, sp in Mage.SPELLS.items():
                        ok = player.mana >= sp["cost"]
                        col = C.WHITE if ok else C.RED
                        box_row(f'  {col}[{sid}] {sp["name"]:22s} {sp["cost"]} MP{C.RESET}')
                        box_row(f'       {C.DIM}{sp["desc"]}{C.RESET}')
                    box_div()
                    box_row(f'  {C.DIM}[0] Volver{C.RESET}')
                    box_bot()
                    sc = input('  > ').strip()
                    if sc == '0': break
                    try: sid = int(sc)
                    except ValueError: continue
                    if sid not in Mage.SPELLS: continue
                    tgt = None if Mage.SPELLS[sid]['type'] == 'heal' else enemy
                    res, msg = player.cast_spell(sid, tgt)
                    if res is None:
                        print(f'\n  {C.RED}{msg}{C.RESET}')
                        pause(1.2)
                        break
                    return f'{C.MAGENTA}{msg}{C.RESET}', True
            else:
                dmg, msg = player.power_strike(enemy)
                if dmg is None:
                    print(f'\n  {C.RED}{msg}{C.RESET}'); pause(1.2); continue
                return f'{C.YELLOW}{C.BRIGHT}{msg}{C.RESET}', True
        if ch == '3' and isinstance(player, Warrior):
            bonus, msg = player.war_cry()
            if bonus is None:
                print(f'\n  {C.RED}{msg}{C.RESET}'); pause(1.2); continue
            return f'{C.CYAN}{C.BRIGHT}{msg}{C.RESET}', True


def _act_menu(enemy) -> tuple:
    """Submenu ACTUAR. Retorna (acted, mensaje, cambio_enojo)."""
    acts = _ENEMY_ACTS.get(enemy.sprite_key,
                           [("Observar", "El enemigo te mira fijamente.", -1)])
    while True:
        clear_screen()
        box_top('  ACTUAR  ')
        box_row()
        for i, (name, _, _) in enumerate(acts):
            box_row(f'  {C.CYAN}[{i+1}]{C.RESET} {name}')
        box_row()
        box_row(f'  {C.DIM}[0] Volver{C.RESET}')
        box_bot()
        ch = input('  > ').strip()
        if ch == '0': return False, '', 0
        try: idx = int(ch) - 1
        except ValueError: continue
        if not (0 <= idx < len(acts)): continue
        name, desc, change = acts[idx]
        clear_screen()
        box_top(f'  ACTUAR: {name}  ')
        box_row()
        box_row(f'  {C.CYAN}{desc}{C.RESET}')
        box_row()
        box_bot()
        pause(2.0)
        return True, f'{C.CYAN}{name}: {desc}{C.RESET}', change


def undertale_combat(player, enemy) -> bool:
    """
    Combate estilo Undertale:
      jugador elige accion → esquiva el ataque del enemigo en tiempo real
    Retorna True si el jugador gano.
    """
    round_num    = 1
    enemy_anger  = 3    # llega a 0 para poder perdonar
    spare_ready  = False

    while player.is_alive and enemy.is_alive:

        # ── Pantalla de accion ──────────────────────────
        _draw_ut_header(player, enemy, round_num)

        spare_col = C.WHITE if spare_ready else C.LGRAY
        print(f'\n  {C.RED}[1] LUCHAR{C.RESET}    '
              f'{C.CYAN}[2] ACTUAR{C.RESET}    '
              f'{C.GREEN}[3] OBJETO{C.RESET}    '
              f'{spare_col}[4] PERDONAR{C.RESET}')
        box_bot()

        choice = input('\n  > ').strip()
        acted  = True
        p_msg  = ''

        if choice == '1':
            p_msg, acted = _fight_menu(player, enemy)

        elif choice == '2':
            acted, p_msg, anger_delta = _act_menu(enemy)
            if acted:
                enemy_anger = max(0, enemy_anger + anger_delta)
                spare_ready = (enemy_anger == 0) or (enemy.hp < enemy.max_hp * 0.25)

        elif choice == '3':
            ok, msg = player.use_potion()
            if not ok:
                print(f'\n  {C.RED}{msg}{C.RESET}'); pause(1.0); acted = False
            else:
                p_msg = f'{C.GREEN}{msg}{C.RESET}'

        elif choice == '4':
            if not spare_ready:
                print(f'\n  {C.LGRAY}El enemigo aun no esta listo para ser perdonado.{C.RESET}')
                pause(1.2); acted = False
            else:
                spare_line = _ENEMY_SPARE_LINES.get(enemy.sprite_key, 'El enemigo se va.')
                if enemy.sprite_key == "dragon":
                    print(f'\n  {C.RED}Malachar no puede ser perdonado.{C.RESET}')
                    pause(1.2); acted = False
                else:
                    clear_screen()
                    box_top('  PERDONAS  ')
                    box_row()
                    box_row(f'  {C.CYAN}{spare_line}{C.RESET}')
                    box_row()
                    xp = enemy.xp_reward // 2
                    box_row(f'  {C.GREEN}+{xp} XP (misericordia){C.RESET}')
                    box_row()
                    box_bot()
                    player.gain_xp(xp)
                    pause(2.5)
                    return True

        if not acted:
            continue

        # ── El enemigo murio con el ataque del jugador ──
        if not enemy.is_alive:
            _draw_ut_header(player, enemy, round_num,
                            log=[p_msg, f'{C.GREEN}{C.BRIGHT}Enemigo derrotado!{C.RESET}'])
            box_bot()
            pause(2.0)
            return True

        # ── Fase de esquiva ─────────────────────────────
        _draw_ut_header(player, enemy, round_num, log=[p_msg])
        box_row(f'  {C.RED}{C.BRIGHT}{enemy.name} prepara su ataque...{C.RESET}')
        box_bot()
        pause(0.9)

        dmg_received = run_dodge_phase(enemy, player)
        player.hp    = max(0, player.hp - dmg_received)

        if not player.is_alive:
            return False

        round_num += 1

    return player.is_alive


# ═══════════════════════════════════════════════════════
#  PANTALLAS DEL JUEGO
# ═══════════════════════════════════════════════════════

def show_title():
    clear_screen()
    box_top()
    box_row()
    art = [
        " _____ _____ ____  __  __ ___ _   _    _    _     ",
        "|_   _| ____|  _ \\|  \\/  |_ _| \\ | |  / \\  | |   ",
        "  | | |  _| | |_) | |\\/| || ||  \\| | / _ \\ | |   ",
        "  | | | |___|  _ <| |  | || || |\\  |/ ___ \\| |___ ",
        "  |_| |_____|_| \\_\\_|  |_|___|_| \\_/_/   \\_\\_____|",
    ]
    for line in art:
        box_row(f'  {C.YELLOW}{C.BRIGHT}{line}{C.RESET}')
    box_row()
    box_row(f'{C.CYAN}{"=== R P G   T E R M I N A L   -   Undertale Edition ===".center(W)}{C.RESET}')
    box_row()
    box_div()
    box_row(f'  {C.DIM}LUCHAR / ACTUAR / OBJETO / PERDONAR{C.RESET}')
    box_row(f'  {C.DIM}Esquiva los ataques enemigos en TIEMPO REAL{C.RESET}')
    box_row()
    box_bot()
    input(f'  {C.BRIGHT}Presiona ENTER para comenzar{C.RESET}')


def create_character():
    clear_screen()
    box_top('  CREACION DE PERSONAJE  ')
    box_row()
    box_row(f'  {C.BRIGHT}Escribe el nombre de tu heroe:{C.RESET}')
    box_bot()
    while True:
        name = input(f'  {C.CYAN}>{C.RESET} ').strip()
        if len(name) >= 2: break
        print(f'  {C.RED}Minimo 2 caracteres.{C.RESET}')

    clear_screen()
    box_top('  ELIGE TU CLASE  ')
    box_row()
    box_row(f'  Bienvenido/a, {C.CYAN}{C.BRIGHT}{name}{C.RESET}.')
    box_row()
    box_div()
    box_row(f'  {C.YELLOW}{C.BRIGHT}[1]  GUERRERO{C.RESET}')
    _draw_side_panel(render_sprite(PLAYER_SPRITES['Guerrero']), [
        ' HP: 140  ATK: 22  DEF: 12',
        ' Golpe Devastador (x2.2) + Grito de Guerra',
        f' {C.DIM}Resistente. Domina el combate cuerpo a cuerpo.{C.RESET}',
    ])
    box_div()
    box_row(f'  {C.MAGENTA}{C.BRIGHT}[2]  MAGO{C.RESET}')
    _draw_side_panel(render_sprite(PLAYER_SPRITES['Mago']), [
        ' HP: 90   MGK: 28  MP: 75',
        ' 4 hechizos: Fuego, Hielo, Curacion, Tormenta',
        f' {C.DIM}Fragil pero devastador. Alto dano magico.{C.RESET}',
    ])
    box_row()
    box_bot()

    while True:
        ch = input(f'  {C.BRIGHT}Elige (1 o 2):{C.RESET} ').strip()
        if ch == '1': player = Warrior(name); break
        if ch == '2': player = Mage(name);    break

    clear_screen()
    box_top(f'  Bienvenido/a, {player.CLASS_NAME} {player.name}!  ')
    box_row()
    player.draw_full()
    box_row()
    box_bot()
    slow_print(f'\n  Tu leyenda comienza ahora, {player.name}...', delay=0.04)
    pause(2.0)
    return player


def show_encounter(enemy: Enemy):
    clear_screen()
    box_top('  ENCUENTRO ENEMIGO!  ')
    box_row()
    enemy.draw()
    box_row()
    box_div()
    box_row(f'  {C.RED}{C.BRIGHT}Un {enemy.name} aparece ante ti!{C.RESET}')
    box_row(f'  {C.DIM}Recompensa: {C.GREEN}{enemy.xp_reward} XP{C.RESET}  '
            f'{C.YELLOW}{enemy.gold} Oro{C.RESET}')
    box_row()
    box_bot()
    pause(2.0)


def show_victory(player, enemy: Enemy):
    clear_screen()
    box_top('  VICTORIA!  ')
    box_row()
    box_row(f'  {C.GREEN}{C.BRIGHT}Has derrotado a {enemy.name}!{C.RESET}')
    box_row()
    box_row(f'  {C.GREEN}+ {enemy.xp_reward} XP{C.RESET}')
    box_row(f'  {C.YELLOW}+ {enemy.gold} monedas de oro{C.RESET}')
    player.gold += enemy.gold

    leveled = player.gain_xp(enemy.xp_reward)
    if leveled:
        box_div()
        box_row(f'  {C.YELLOW}{C.BRIGHT}*** NIVEL {player.level}! Stats mejorados! ***{C.RESET}')

    heal = player.max_hp // 5
    player.heal(heal)
    box_row(f'  {C.GREEN}Recuperas {heal} HP.{C.RESET}')

    if isinstance(player, Mage):
        player.restore_mana(15)
        box_row(f'  {C.CYAN}+15 MP recuperados.{C.RESET}')
    elif isinstance(player, Warrior):
        player.stamina = min(player.stamina + 1, player.max_stamina)
        box_row(f'  {C.YELLOW}+1 Stamina recuperada.{C.RESET}')

    if player.potions < 5 and random.random() < 0.35:
        player.potions += 1
        box_row(f'  {C.GREEN}Encuentras una Pocion! ({player.potions} total){C.RESET}')

    box_div()
    player.draw_full()
    box_row()
    box_bot()
    pause(2.5)


def show_game_over(player):
    clear_screen()
    box_top()
    box_row()
    for row in ["RRRRRR..RR....RR..RRRRRR..RRRRRR","RR......RRR...RR..RR......RR.....","RRRR....RRRR..RR..RRRR....RRRR..","RR......RR.RR.RR..RR......RR.....","RRRRRR..RR..RRRR..RRRRRR..RRRRRR"]:
        colored = '  ' + C.RED + C.BRIGHT + row.replace('R','█').replace('.', ' ') + C.RESET
        print('║' + colored + ' ' * max(0, W - _visible_len(colored)) + '║')
    box_row()
    box_div()
    box_row(f'  {player.name} ha caido en batalla...')
    box_row(f'  Nivel alcanzado: {C.YELLOW}{player.level}{C.RESET}')
    box_row(f'  Oro acumulado:   {C.YELLOW}{player.gold}{C.RESET}')
    box_row()
    box_bot()
    input('  Presiona ENTER para continuar...')


# ═══════════════════════════════════════════════════════
#  SISTEMA DE HISTORIA (paginado por párrafo)
# ═══════════════════════════════════════════════════════

def _type_line(text: str, color: str = '', delay: float = 0.021):
    sys.stdout.write(f'║  {color}')
    sys.stdout.flush()
    for ch in text:
        sys.stdout.write(ch); sys.stdout.flush(); time.sleep(delay)
    sys.stdout.write(f'{C.RESET}' + ' ' * max(0, W - 2 - len(text)) + '║\n')
    sys.stdout.flush()

def _subst(text: str, player) -> str:
    if not player: return text
    arma = 'espada' if isinstance(player, Warrior) else 'baculo magico'
    return (text.replace('[nombre]', player.name)
                .replace('[clase]',  player.CLASS_NAME)
                .replace('[arma]',   arma))

def story_screen(title: str, sections: list, player=None, delay: float = 0.021):
    """Divide en paginas por lineas en blanco. ENTER para avanzar cada pagina."""
    pages, cur = [], []
    for color, text in sections:
        if color == '' and text == '':
            if cur: pages.append(cur); cur = []
        else:
            cur.append((color, text))
    if cur: pages.append(cur)

    for idx, page in enumerate(pages):
        clear_screen()
        box_top(f'  {title}  ')
        box_row()
        for color, text in page:
            if color == 'div': box_div()
            else: _type_line(_subst(text, player), color, delay)
        box_row()
        box_bot()
        sfx = f'({idx+1}/{len(pages)})' if idx < len(pages) - 1 else ''
        input(f'  {C.DIM}[ ENTER para continuar {sfx}]{C.RESET}')


# ── Historia ──────────────────────────────────────────

_STORY_OPENING = [
    (C.LRED,   'Las llamas de Valhart iluminan la noche como un sol negro.'),
    ('',''),
    (C.WHITE,  'Tu aldea -- que durante generaciones fue un lugar de paz --'),
    (C.WHITE,  'arde. Los gritos de tus vecinos se mezclan con el crujido'),
    (C.WHITE,  'de la madera ardiendo y el rugido de algo antiguo y terrible.'),
    ('',''),
    (C.DIM,    'Hace tres lunas, el Senor del Abismo --MALACHAR-- desperto.'),
    (C.DIM,    'Su aliento corrompio los bosques. Sus garras aplastaron ciudades.'),
    (C.DIM,    'Su magia negra resucito a los muertos para que le sirvieran.'),
    ('',''),
    (C.WHITE,  'Entre el caos, una mano te agarra del brazo.'),
    (C.WHITE,  'El Anciano Thariel. Sus ojos, siempre serenos, ahora arden.'),
    ('',''),
    (C.CYAN,   '  "Escucha. Las estrellas lo dijeron hace veinte anos."'),
    (C.CYAN,   '  "UN heroe. UN camino. Eldoria no puede ser salvada por ejercitos."'),
    ('',''),
    (C.WHITE,  'Te pone tu [arma] en las manos.'),
    ('',''),
    (C.CYAN,   '  "Malachar mora al norte. Bosques, Ruinas, Ciudadela. Y al final... el."'),
    (C.CYAN,   '  "No mires atras, [nombre]. Valhart ya no existe."'),
    (C.CYAN,   '  "Pero Eldoria... Eldoria todavia puede existir."'),
    ('',''),
    (C.DIM,    'Una viga ardiendo cae entre los dos. Cuando el humo se disipa,'),
    (C.DIM,    'Thariel ya no esta. Solo quedan las llamas. Y el camino norte.'),
    ('',''),
    (C.LYELLOW,'Sin mirar atras, te adentras en la oscuridad.'),
]

_ACT_INTROS = {
    1: [
        (C.LGRAY,  'Los Bosques de Grenmoor.'),
        ('',''),
        (C.WHITE,  'Hace dos semanas eran un lugar de belleza salvaje.'),
        (C.WHITE,  'Pajaros de cien colores. Arboles centenarios.'),
        (C.WHITE,  'Un rio de agua tan clara que veias el fondo a tres metros.'),
        ('',''),
        (C.WHITE,  'Ahora los arboles estan retorcidos. El suelo exhala vapor violaceo.'),
        (C.WHITE,  'El rio fluye negro. Y en las sombras...'),
        ('',''),
        (C.LRED,   '                  ...se mueven cosas.'),
        ('',''),
        (C.DIM,    'Aprietas tu [arma]. Y avanzas.'),
    ],
    2: [
        (C.LGRAY,  'Las Ruinas de Valdris.'),
        ('',''),
        (C.WHITE,  'Fue en su dia la ciudad mas grande de Eldoria.'),
        (C.WHITE,  'Torres de cristal. Los magos mas sabios del mundo conocido.'),
        ('',''),
        (C.DIM,    'Ahora no queda nada. Solo piedra negra y el eco'),
        (C.DIM,    'de los que vivieron aqui -- obligados a vagar sin descanso.'),
        ('',''),
        (C.LRED,   'Los muertos no descansan. Y pronto te encontraran.'),
    ],
    3: [
        (C.LGRAY,  'La Ciudadela Oscura.'),
        ('',''),
        (C.WHITE,  'Sus torres rasgan el cielo. Cadenas de cien metros cuelgan'),
        (C.WHITE,  'con criaturas sujetas. Muros de treinta metros de grosor.'),
        ('',''),
        (C.YELLOW, 'Llegaste hasta aqui, [nombre].'),
        (C.YELLOW, 'Atravesaste el bosque. Cruzaste las ruinas. Sobreviviste todo.'),
        ('',''),
        (C.LYELLOW,'Una batalla mas. La ultima. Exhalas. Y entras.'),
    ],
}

_MID_ACT = {
    1: [
        (C.WHITE,  'Entre la maleza, escuchas algo humano. Una tos.'),
        ('',''),
        (C.WHITE,  'Detras de un arbol caido: una mujer joven, herida, con capa de viajera.'),
        (C.WHITE,  'Al verte, su mano va instintivamente a un cuchillo.'),
        ('',''),
        (C.CYAN,   '  "Espera -- no soy una de esas cosas."'),
        ('',''),
        (C.CYAN,   '  "Soy Lyra. Exploradora del Rey. O lo era, antes de que"'),
        (C.CYAN,   '   el Rey ya no existiera. Llevo dias aqui."'),
        ('',''),
        (C.CYAN,   '  "Si vas al norte... la magia de Malachar se alimenta del miedo.'),
        (C.CYAN,   '   Si no tienes miedo... su poder sobre ti disminuye."'),
        ('',''),
        (C.DIM,    'Se pierde entre los arboles. Tu sigues hacia el norte.'),
    ],
    2: [
        (C.WHITE,  'Entre las ruinas de una torre, una figura aparece. Semi-transparente.'),
        ('',''),
        (C.WHITE,  'Un hombre anciano. Ojos blancos y puros. Un fantasma con paz.'),
        ('',''),
        (C.CYAN,   '  "Fui el Gran Archimago de Valdris. Malachar me mato hace dos semanas."'),
        (C.CYAN,   '  "Pero me niego a servir a ese monstruo."'),
        ('',''),
        (C.CYAN,   '  "La Ciudadela tiene una camara interior. El corazon de Malachar late ahi."'),
        (C.CYAN,   '  "Cuando llegues a el... usa todo lo que tienes. Sin reservas."'),
        ('',''),
        (C.DIM,    'La figura desaparece. Solo quedan las ruinas y el silencio.'),
    ],
    3: [
        (C.WHITE,  'En un calabozo, una voz debil te llama por tu nombre.'),
        ('',''),
        (C.WHITE,  'El General Aldric. Capturado hace una semana. Flaco pero con ojos encendidos.'),
        ('',''),
        (C.CYAN,   '  "Eres real. Gracias a los dioses, eres real."'),
        ('',''),
        (C.CYAN,   '  "Malachar puede hablar. Intentara convencerte de rendirte."'),
        (C.CYAN,   '  "NADA de lo que diga es verdad. No lo escuches."'),
        ('',''),
        (C.WHITE,  'Te da una pocion. Te estrecha la mano.'),
        ('',''),
        (C.CYAN,   '  "Vence por todos nosotros, [nombre]."'),
    ],
}

_ACT_OUTROS = {
    1: [
        (C.WHITE,  'Al salir del bosque encuentras a un guardia real tendido en el suelo.'),
        (C.WHITE,  'Una flecha negra en su costado. Todavia vivo. Por poco.'),
        ('',''),
        (C.CYAN,   '  "Tu... lograste cruzar el bosque solo."'),
        (C.CYAN,   '  "Las Ruinas de Valdris. Al norte. Los muertos caminan."'),
        (C.CYAN,   '  "Dile a mi familia... que mori bien."'),
        ('',''),
        (C.DIM,    'Cierra los ojos. Una ultima respiracion.'),
        ('',''),
        (C.LYELLOW,'Miras al norte. Las Ruinas aguardan.'),
    ],
    2: [
        (C.WHITE,  'Una anciana emerge de detras de un muro. Lampara de aceite en la mano.'),
        ('',''),
        (C.CYAN,   '  "Por los dioses... ALGUIEN LLEGO. ALGUIEN LLEGO."'),
        ('',''),
        (C.CYAN,   '  "Soy Marta, la bibliotecaria de Valdris. Llevo dos semanas escondida."'),
        (C.CYAN,   '  "Vi como mataban a todos. Vi como los muertos se levantaban."'),
        ('',''),
        (C.CYAN,   '  "Pero nunca... nunca perdi la esperanza."'),
        (C.CYAN,   '  "Llegaste hasta aqui, [nombre]. TU LLEGASTE."'),
        ('',''),
        (C.WHITE,  'Te da una pocion. La ultima que le quedaba.'),
        ('',''),
        (C.LYELLOW,'La Ciudadela Oscura corta el cielo al frente.'),
    ],
    3: [
        (C.WHITE,  'El ultimo guardian cae. El silencio es total.'),
        ('',''),
        (C.WHITE,  'Frente a ti: una puerta de obsidiana de cinco metros.'),
        (C.WHITE,  'Sin manija. Sin cerrojo. Empieza a abrirse sola.'),
        ('',''),
        (C.LRED,   'El calor que sale es insoportable. Olor a azufre.'),
        ('',''),
        (C.WHITE,  'Y desde las profundidades, una respiracion.'),
        (C.WHITE,  'Lenta. Profunda. Como truenos encadenados.'),
        ('',''),
        (C.RED,    '                  MALACHAR te espera.'),
    ],
}

_BOSS_INTRO = [
    (C.LGRAY,  'La camara es mas grande que cualquier sala que hayas visto.'),
    (C.LGRAY,  'El techo desaparece en la oscuridad arriba.'),
    ('',''),
    (C.WHITE,  'Y entonces... dos ojos se abren en la penumbra.'),
    ('',''),
    (C.LRED,   'Como soles incandescentes. Rojos. Antiguos. Hambrientos.'),
    ('',''),
    (C.WHITE,  'Una figura colosal se levanta. Despliega alas negras que bloquean la luz.'),
    (C.WHITE,  'Su cuerpo: armadura de escamas rojas con fuego interior.'),
    ('',''),
    (C.RED,    '  "...Un [clase]."'),
    ('',''),
    (C.RED,    '  "Eldoria me envia un [clase]. Llamado [nombre]."'),
    ('',''),
    (C.RED,    '  "Mate a reyes. Destrui ejercitos. Aplaste a los magos de Valdris."'),
    (C.RED,    '  "Y me envian a UN [clase]."'),
    ('',''),
    (C.WHITE,  'Abre las fauces. El fuego ilumina la camara de rojo sangriento.'),
    ('',''),
    (C.RED,    '  "Al menos tendre el honor de borrarte del mundo yo mismo."'),
    ('',''),
    (C.LYELLOW,'Empunas tu [arma]. No tienes miedo. Ya no importa si lo tienes.'),
]

_STORY_ENDING = [
    (C.WHITE,  'Malachar cae.'),
    ('',''),
    (C.WHITE,  'El impacto sacude la montana. Las cadenas de su maldicion se rompen'),
    (C.WHITE,  'con un sonido que sientes hasta en los huesos.'),
    ('',''),
    (C.LGRAY,  'El dragon te mira desde el suelo. Sus ojos ya no son brasas.'),
    (C.LGRAY,  'Solo un cansancio que trasciende los siglos.'),
    ('',''),
    (C.RED,    '  "Imposible..."'),
    ('',''),
    (C.RED,    '  "Cien anos de poder. Y un [clase] llamado [nombre]..."'),
    ('',''),
    (C.LGRAY,  'Sus escamas pierden el brillo carmesi, una a una. Como hojas en otono.'),
    ('',''),
    (C.RED,    '  "Eldoria... sobrevivira... despues de todo..."'),
    ('',''),
    (C.LGRAY,  'Y cierra los ojos para siempre.'),
    ('',''),
    (C.WHITE,  'Afuera, el cielo negro de Malachar comienza a disolverse.'),
    (C.WHITE,  'La luz del sol -- que no se habia visto en semanas -- rompe las nubes.'),
    ('',''),
    (C.WHITE,  'En Eldoria, la gente sale a las calles mirando al cielo con lagrimas.'),
    (C.WHITE,  'En Valdris, los muertos dejan de moverse. Uno a uno. Y caen.'),
    (C.WHITE,  'Esta vez para siempre. Esta vez con paz.'),
    ('',''),
    (C.YELLOW, 'Nadie sabe todavia tu nombre.'),
    (C.YELLOW, 'Nadie sabe lo que hiciste hoy.'),
    ('',''),
    (C.LYELLOW,'Pero muy pronto... todos lo sabran.'),
    ('',''),
    (C.BRIGHT, '                    F I N'),
]

_BETWEEN_BATTLE = {
    1: ['Te limpias el [arma]. El bosque continua.',
        'Dos menos. El corazon del bosque aun aguarda.',
        'Casi al otro lado. Solo queda uno mas.',
        'El bosque queda atras. Lo lograste.'],
    2: ['Los muertos no cesan. Pero su numero merma.',
        'Las ruinas se abren paso entre las sombras.',
        'Casi al otro lado. La Ciudadela es visible.',
        'El ultimo obstaculo de Valdris cae. Respiras.'],
    3: ['Un guardian menos. Las antorchas tiemblan.',
        'Los pasillos se hacen mas oscuros.',
        'La resistencia es feroz. Pero no suficiente.',
        'El camino a la camara de Malachar esta casi despejado.'],
}


def _subst_plain(text: str, player) -> str:
    if not player: return text
    arma = 'espada' if isinstance(player, Warrior) else 'baculo'
    return text.replace('[nombre]', player.name).replace('[clase]', player.CLASS_NAME).replace('[arma]', arma)

def between_battle_screen(player, act: int, battle_num: int, total: int):
    clear_screen()
    box_top(f'  Batalla {battle_num} de {total} superada  ')
    box_row()
    texts = _BETWEEN_BATTLE.get(act, [])
    idx   = min(battle_num - 1, len(texts) - 1)
    if 0 <= idx < len(texts):
        box_row(f'  {C.DIM}{_subst_plain(texts[idx], player)}{C.RESET}')
        box_row()
    player.draw_full()
    box_row()
    box_div()
    heal = player.max_hp // 4
    player.heal(heal)
    box_row(f'  {C.GREEN}Descansas. +{heal} HP.{C.RESET}')
    if isinstance(player, Mage):
        player.restore_mana(10)
        box_row(f'  {C.CYAN}+10 MP.{C.RESET}')
    if isinstance(player, Warrior):
        player.stamina = min(player.stamina + 1, player.max_stamina)
        box_row(f'  {C.YELLOW}+1 Stamina.{C.RESET}')
    box_row()
    box_row(f'  {C.GREEN}[1]{C.RESET} Continuar avanzando')
    box_row(f'  {C.CYAN}[2]{C.RESET} Ver estado completo')
    box_row()
    box_bot()
    while True:
        c = input('  > ').strip()
        if c == '1': break
        if c == '2':
            clear_screen(); box_top('  ESTADO  '); box_row()
            player.draw_full(); box_row(); box_bot()
            input(f'  {C.DIM}[ ENTER ]{C.RESET}')
            break


def act_full_heal(player):
    player.hp = player.max_hp
    if isinstance(player, Mage): player.mana = player.max_mana
    if isinstance(player, Warrior): player.stamina = player.max_stamina
    if player.potions < 3: player.potions = 3


def run_act(player, act_num: int) -> bool:
    titles = {1: 'ACTO I  -  Los Bosques de Grenmoor',
              2: 'ACTO II  -  Las Ruinas de Valdris',
              3: 'ACTO III  -  La Ciudadela Oscura'}
    title = titles[act_num]

    story_screen(title, _ACT_INTROS[act_num], player=player)

    for n in range(1, 5):
        enemy = get_act_enemy(act_num)
        show_encounter(enemy)
        if not undertale_combat(player, enemy):
            show_game_over(player); return False
        show_victory(player, enemy)
        if n == 2:
            story_screen(title, _MID_ACT[act_num], player=player)
        if n < 4:
            between_battle_screen(player, act_num, n, 4)

    story_screen(title, _ACT_OUTROS[act_num], player=player)
    act_full_heal(player)
    return True


def run_boss(player) -> bool:
    story_screen('MALACHAR, SENOR DEL ABISMO', _BOSS_INTRO, player=player, delay=0.026)
    malachar = get_malachar()
    show_encounter(malachar)
    if undertale_combat(player, malachar):
        show_victory(player, malachar)
        story_screen('EL FIN DE LA OSCURIDAD', _STORY_ENDING, player=player, delay=0.026)
        return True
    show_game_over(player)
    return False


# ═══════════════════════════════════════════════════════
#  BUCLE PRINCIPAL
# ═══════════════════════════════════════════════════════

def game_loop():
    show_title()
    while True:
        story_screen('PROLOGO', _STORY_OPENING)
        player = create_character()

        survived = True
        for act_num in [1, 2, 3]:
            if not run_act(player, act_num):
                survived = False; break

        if survived:
            run_boss(player)

        print(f'\n  {C.BRIGHT}Nueva aventura? (s/n):{C.RESET} ', end='')
        if input().strip().lower() != 's':
            clear_screen()
            box_top('  HASTA LA PROXIMA!  ')
            box_row(f'  Gracias por jugar, {C.CYAN}{player.name}{C.RESET}.')
            box_row(f'  Nivel alcanzado: {C.YELLOW}{player.level}{C.RESET}')
            box_row(f'  Oro total:       {C.YELLOW}{player.gold}{C.RESET}')
            box_row()
            box_bot()
            pause(1.5)
            break


if __name__ == '__main__':
    game_loop()
