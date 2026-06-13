# -*- coding: utf-8 -*-
from colors import C

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
