# -*- coding: utf-8 -*-
from colors import C
from characters import Warrior, Mage
from enemies import _ENEMY_ACTS, _ENEMY_SPARE_LINES
from ui import box_top, box_div, box_bot, box_row, pause, clear_screen
from dodge import run_dodge_phase


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
                while True:
                    clear_screen()
                    box_top('  GRIMORIO  ')
                    box_row(f'  {C.CYAN}Mana: {player.mana}/{player.max_mana}{C.RESET}')
                    box_div()
                    for sid, sp in Mage.SPELLS.items():
                        ok  = player.mana >= sp["cost"]
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
    round_num    = 1
    enemy_anger  = 3
    spare_ready  = False

    while player.is_alive and enemy.is_alive:

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

        if not enemy.is_alive:
            _draw_ut_header(player, enemy, round_num,
                            log=[p_msg, f'{C.GREEN}{C.BRIGHT}Enemigo derrotado!{C.RESET}'])
            box_bot()
            pause(2.0)
            return True

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
