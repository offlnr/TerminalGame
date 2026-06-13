# -*- coding: utf-8 -*-
import random

from colors import C
from sprites import ENEMY_SPRITES, render_sprite
from ui import hp_bar, _draw_side_panel


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
    "slime":     ("Slime",         40,  22,  1,  45,  4, "slime",     C.CYAN),
    "goblin":    ("Goblin",        50,  34,  2,  60,  6, "goblin",    C.GREEN),
    "wolf":      ("Lobo Feroz",    60,  50,  3,  70,  8, "wolf",      C.YELLOW),
    "skeleton":  ("Esqueleto",     70,  46,  6,  80,  9, "skeleton",  C.WHITE),
    "orc":       ("Orco Guerrero", 105, 58, 10, 110, 16, "orc",       C.LGREEN),
    "dark_mage": ("Mago Oscuro",   80,  64,  5, 130, 20, "dark_mage", C.MAGENTA),
    "troll":     ("Troll de Roca", 125, 54, 13, 150, 24, "troll",     C.LGRAY),
    "vampire":   ("Vampiro",       90,  56,  7, 140, 22, "vampire",   C.LMAGENTA),
    "demon":     ("Demonio Mayor", 110, 72,  8, 160, 28, "demon",     C.RED),
}


def get_act_enemy(act: int) -> Enemy:
    pools = {1: ["slime", "goblin", "wolf"],
             2: ["wolf", "skeleton", "orc"],
             3: ["dark_mage", "troll", "vampire", "demon"]}
    key = random.choice(pools.get(act, ["goblin"]))
    n, hp, atk, dfn, xp, gold, skey, color = _TEMPLATES[key]
    return Enemy(n, hp, atk, dfn, xp, gold, skey, color)


def get_malachar() -> Enemy:
    return Enemy("Malachar, Senor del Abismo", 250, 40, 16, 600, 999, "dragon", C.RED)


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
