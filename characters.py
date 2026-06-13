# -*- coding: utf-8 -*-
import random

from colors import C
from sprites import PLAYER_SPRITES, render_sprite
from ui import (box_row, hp_bar, mp_bar, xp_bar, stamina_pips,
                _draw_side_panel)


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
        raw = int(self.attack * random.uniform(0.50, 0.80))
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
        raw = int(self.attack * 0.8 * random.uniform(0.80, 1.05))
        dmg = target.take_damage(raw)
        return dmg, f'GOLPE DEVASTADOR! {dmg} dano.'

    def war_cry(self) -> tuple:
        if self.stamina < 2:
            return None, 'Necesitas 2 Stamina.'
        self.stamina -= 2
        bonus = int(self.attack * 0.08)
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
        1: {"name": "Bola de Fuego",   "cost": 15, "mult": 0.65, "type": "damage", "desc": "Dano de fuego moderado"},
        2: {"name": "Rayo de Hielo",   "cost": 10, "mult": 0.40, "type": "damage", "desc": "Bajo costo, dano bajo"},
        3: {"name": "Curacion Arcana", "cost": 20, "mult": 1.1,  "type": "heal",   "desc": "Restaura HP propio"},
        4: {"name": "Tormenta Arcana", "cost": 30, "mult": 0.90, "type": "damage", "desc": "El hechizo mas potente"},
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
        box_row(f'  MP {mp_bar(self.mana, self.max_mana)} {self.mana}/{self.max_mana}'
                f'   XP {xp_bar(self.xp, self.xp_to_next)}')

    def draw_full(self):
        lines = render_sprite(PLAYER_SPRITES[self.SPRITE_KEY])
        stats = [
            f' {C.MAGENTA}{C.BRIGHT}{self.CLASS_NAME}: {self.name}{C.RESET}  Nv.{self.level}',
            f' HP  {hp_bar(self.hp, self.max_hp, 16)} {self.hp}/{self.max_hp}',
            f' MP  {mp_bar(self.mana, self.max_mana, 16)} {self.mana}/{self.max_mana}',
            f' XP  {xp_bar(self.xp, self.xp_to_next)} {self.xp}/{self.xp_to_next}',
            f' MGK {self.magic_power}   DEF {self.defense}',
            f' {C.GREEN}Pociones: {self.potions}{C.RESET}   Oro: {self.gold}',
        ]
        _draw_side_panel(lines, stats)
