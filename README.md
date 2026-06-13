<img width="508" height="234" alt="image" src="https://github.com/user-attachments/assets/11c0c496-d015-4a31-9879-dd30dc83e290" /># Terminal RPG

A turn-based RPG that runs entirely in the terminal, featuring **Undertale-style real-time dodge combat**, Unicode pixel art sprites, and an epic 3-act story.

## Requirements

- Python 3.8+
- Windows 10/11 (the real-time dodge system uses `msvcrt`)

```bash
pip install colorama
```

## How to play

```bash
python game.py
```

## Combat

Each turn you have 4 options:

| Option | Description |
|--------|-------------|
| `FIGHT` | Attack the enemy (physical, skills, or spells) |
| `ACT` | Interact with the enemy to reduce their hostility |
| `ITEM` | Use a health potion |
| `SPARE` | Spare the enemy once they are calm enough |

After every player action, the enemy counterattacks with a **real-time dodge mini-game**: move your soul `♥` using `W A S D` or the arrow keys to dodge incoming projectiles. Dodge everything and you take **0 damage**.

## Classes

**Warrior**
- High HP and defense
- Power Strike (2.2× damage, costs Stamina)
- War Cry (permanently boosts ATK for the current fight)

**Mage**
- Four spells: Fireball, Ice Ray, Arcane Heal, Arcane Storm
- Lower defense but devastating magic damage

## Content

- 3 acts with 4 battles each + a mid-act cutscene
- 9 enemy types, each with a unique attack pattern
- Final boss: **Malachar, Lord of the Abyss**
- ACT system: every enemy has 2 unique interactions that can lead to sparing them
- Full story with prologue, inter-act scenes and ending — text advances paragraph by paragraph at your own pace

## Enemies & attack patterns

| Enemy | Pattern |
|-------|---------|
| Slime | Slow blobs falling from above |
| Goblin | Fast arrows from right to left |
| Wolf | Diagonal strikes from the corner |
| Skeleton | Bones from both sides simultaneously |
| Orc | Wide, slow wall projectile |
| Dark Mage | Curving orbs, doubles in later phase |
| Troll | Irregular rocks, accelerates over time |
| Vampire | Bats from any side |
| Demon | Fast projectiles from all 4 edges |
| **Malachar** | Wall of fire with a single gap — find it |

