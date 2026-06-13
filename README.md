# Terminal RPG

Un juego de rol por turnos que corre completamente en la terminal, con combate en tiempo real al estilo **Undertale**, pixel art con bloques Unicode y una historia épica de 3 actos.

## Requisitos

- Python 3.8+
- Windows 10/11 (el sistema de esquiva en tiempo real usa `msvcrt`)

```bash
pip install colorama
```

## Cómo jugar

```bash
python game.py
```

## Combate

Cada turno tienes 4 opciones:

| Opción | Descripción |
|--------|-------------|
| `LUCHAR` | Ataca al enemigo (físico, habilidades o hechizos) |
| `ACTUAR` | Interactúa con el enemigo para reducir su hostilidad |
| `OBJETO` | Usa una poción de salud |
| `PERDONAR` | Perdona al enemigo cuando está lo suficientemente calmado |

Después de cada acción del jugador, el enemigo contraataca con un **mini-juego de esquiva en tiempo real**: mueve tu alma `♥` con `W A S D` o las flechas del teclado para esquivar los proyectiles. Si los esquivas todos, recibes **0 daño**.

## Clases

**Guerrero**
- HP alto, defensa alta
- Golpe Devastador (x2.2 daño, consume Stamina)
- Grito de Guerra (aumenta ATK permanentemente en el combate)

**Mago**
- Cuatro hechizos: Bola de Fuego, Rayo de Hielo, Curación Arcana, Tormenta Arcana
- Menor defensa pero mayor daño mágico

## Contenido

- 3 actos con 4 combates cada uno + escena narrativa a mitad de acto
- 9 tipos de enemigos, cada uno con patrón de ataque único
- Jefe final: **Malachar, Señor del Abismo**
- Sistema ACT: cada enemigo tiene 2 acciones propias que permiten perdonarlo
- Prólogo, historia entre actos y final completo con texto al ritmo del jugador (ENTER por párrafo)

## Enemigos y patrones de ataque

| Enemigo | Patrón |
|---------|--------|
| Slime | Bolas lentas cayendo desde arriba |
| Goblin | Flechas rápidas de derecha a izquierda |
| Lobo | Ataques diagonales desde la esquina |
| Esqueleto | Huesos desde ambos lados simultáneamente |
| Orco | Pared ancha y lenta |
| Mago Oscuro | Orbes curvos, dobles en fase tardía |
| Troll | Rocas irregulares, se vuelve más rápido |
| Vampiro | Murciélagos desde cualquier lado |
| Demonio | Proyectiles rápidos desde los 4 bordes |
| **Malachar** | Pared de fuego con un único hueco — encuéntralo |

## Capturas

```
╔══════════════════════════════════════════════════════════════════════╗
║                      COMBATE  -  Ronda 3                            ║
║                                                                      ║
║      ██████          Goblin                                          ║
║      ██  ██          HP  ████████░░░░░░░░░░ 28/50                   ║
║      ████            ATK 10   DEF 2                                  ║
╠══════════════════════════════════════════════════════════════════════╣
║  GOLPE DEVASTADOR! 44 dano.                                          ║
╠══════════════════════════════════════════════════════════════════════╣
║  Guerrero: Aldric  Nv.2  HP ██████████████░░░░░░ 98/140  [P:2]      ║
╚══════════════════════════════════════════════════════════════════════╝

*** ATAQUE DE GOBLIN ***
Tiempo: ████████████░░░░░░░░░░░░░░░░░░
HP:     ██████████████████░░ 98/140

┌──────────────────────────────┐
│                  >           │
│       >                      │
│                    >         │
│            ♥                 │
│    >                         │
│                >             │
│          >                   │
│                              │
└──────────────────────────────┘
Mueve: W A S D  o  flechas del teclado
```
