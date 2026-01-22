"""
Constantes para el Tetris con Pygame.
"""


TAMANO_VENTANA = 640, 480
DIM_PLATAFORMA = 10, 20
BORDE_PLATAFORMA = 4
TAMANO_BLOQUE = 20, 20


TAMANO_PLATAFORMA = tuple([DIM_PLATAFORMA[i]*TAMANO_BLOQUE[i] for i in range(2)])
TAMANO_PLABORD = tuple([DIM_PLATAFORMA[i]*TAMANO_BLOQUE[i]+BORDE_PLATAFORMA*2 for i in range(2)])

MARGEN = tuple([TAMANO_VENTANA[i]-TAMANO_PLATAFORMA[i]- BORDE_PLATAFORMA*2 for i in range(2)])
START_PLATAFORMA = int(MARGEN[0]/2), MARGEN[1]+2*BORDE_PLATAFORMA
START_PLABORD = int(MARGEN[0]/2)-BORDE_PLATAFORMA, MARGEN[1]+BORDE_PLATAFORMA

CENTRO_VENTANA = tuple([TAMANO_VENTANA[i]/2 for i in range(2)])
POS = CENTRO_VENTANA[0], CENTRO_VENTANA[1]+100
POSICION_SCORE = TAMANO_VENTANA[0] - START_PLABORD[0] / 2, 120
POSICION_PIEZAS = POSICION_SCORE[0], 150
POSICION_LINEAS = POSICION_SCORE[0], 180
POSICION_TETRIS = POSICION_SCORE[0], 210
POSICION_NIVEL = POSICION_SCORE[0], 240

GRAVEDAD = 0.35



PIEZAS = {
    'O': [
        '0000\n0110\n0110\n0000',
    ],
    'S': [
        '0000\n0022\n0220\n0000',
        '0000\n0200\n0220\n0020',
    ],
    'Z': [
        '0000\n3300\n0330\n0000',
        '0000\n0030\n0330\n0300',
    ],
    'I': [
        '0400\n0400\n0400\n0400',
        '0000\n4444\n0000\n0000',
    ],
    'J': [
        '0000\n5000\n5550\n0000',
        '0000\n0550\n0500\n0500',
        '0000\n0000\n5550\n0050',
        '0000\n0050\n0050\n0550',
    ],
    'L': [
        '0000\n0060\n6660\n0000',
        '0000\n0060\n0060\n0660',
        '0000\n0000\n6660\n6000',
        '0000\n0660\n0060\n0060',
    ],
    'T': [
        '0000\n0700\n7770\n0000',
        '0000\n0700\n0770\n0700',
        '0000\n0000\n7770\n0700',
        '0000\n0070\n0770\n0070',
    ]
}



# for k, v in PIEZAS.items():
#     print(k)
#     for p in v:
#         print(p + '\n')





COLORES = {
    0: (0, 0, 0),
    1: (255, 255, 0),
    2: (0, 255, 0),
    3: (255, 0, 0),
    4: (0, 255, 255),
    5: (0, 0, 255),
    6: (255, 127, 0),
    7: (255, 0, 255),
    8: (127, 255, 0),
    9: (255, 255, 255),
}



for name, rotations in PIEZAS.items():
    PIEZAS[name] = [ [ [int(i) for i in p] for p in r.splitlines()] for r in rotations]








PIEZAS_KEYS = list(PIEZAS.keys())