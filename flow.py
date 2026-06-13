# -*- coding: utf-8 -*-
from colors import C
from characters import Warrior, Mage
from enemies import get_act_enemy, get_malachar
from ui import clear_screen, pause, box_top, box_div, box_bot, box_row
from screens import show_encounter, show_victory, show_game_over
from combat import undertale_combat
from story import (story_screen, _BETWEEN_BATTLE, _ACT_INTROS, _MID_ACT,
                   _ACT_OUTROS, _BOSS_INTRO, _STORY_ENDING, _STORY_OPENING)


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


def game_loop():
    from screens import show_title, create_character
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
