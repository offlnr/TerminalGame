# -*- coding: utf-8 -*-
import random

from colors import C
from characters import Warrior, Mage
from enemies import Enemy
from sprites import PLAYER_SPRITES, render_sprite
from ui import (clear_screen, pause, slow_print, box_top, box_div, box_bot,
                box_row, hp_bar, _draw_side_panel, _visible_len, W)


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
    for row in ["RRRRRR..RR....RR..RRRRRR..RRRRRR", "RR......RRR...RR..RR......RR.....",
                "RRRR....RRRR..RR..RRRR....RRRR..", "RR......RR.RR.RR..RR......RR.....",
                "RRRRRR..RR..RRRR..RRRRRR..RRRRRR"]:
        colored = '  ' + C.RED + C.BRIGHT + row.replace('R', '█').replace('.', ' ') + C.RESET
        print('║' + colored + ' ' * max(0, W - _visible_len(colored)) + '║')
    box_row()
    box_div()
    box_row(f'  {player.name} ha caido en batalla...')
    box_row(f'  Nivel alcanzado: {C.YELLOW}{player.level}{C.RESET}')
    box_row(f'  Oro acumulado:   {C.YELLOW}{player.gold}{C.RESET}')
    box_row()
    box_bot()
    input('  Presiona ENTER para continuar...')
