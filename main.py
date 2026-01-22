import random
import time
import pygame
import sys
from pygame.locals import *
from constantes import *


class Juego:

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode(TAMANO_VENTANA)
        self.fonts = {
            'defaut': pygame.font.Font('freesansbold.ttf', 18),
            'title': pygame.font.Font('freesansbold.ttf', 100),
        }

        pygame.display.set_caption('Tetris')
        

    def start(self):
        self.surface.fill((0, 0, 0))  # fondo negro (o tu color)
        self._mostrarTexto('Tetris', CENTRO_VENTANA, font='title')
        self._mostrarTexto('Presiona cualquier tecla para jugar', POS)
        self._espera()

    def _salir(self):
        print("Salir")
        pygame.quit()
        sys.exit()

    def _render(self):
        pygame.display.update()          # o flip()
        self.clock.tick(60)              # limita a 60 FPS

    def stop(self):
        self._mostrarTexto('Perdido', CENTRO_VENTANA, font='title')
        self._espera()
        self._salir()

    def _getEvent(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self._salir()
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    self._salir()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    continue
                return event.key

    def _mostrarTexto(self, text, position, color=9, font='defaut'):
#        print("Mostrar texto")
        font = self.fonts.get(font, self.fonts['defaut'])
        color = COLORES.get(color, COLORES[9])
        devuelto = font.render(text, True, color)
        rect = devuelto.get_rect()
        rect.center = position
        self.surface.blit(devuelto, rect)

    def _espera(self):
        print("Espera")
        while self._getEvent() == None:
            self._render()

    def _getPieza(self):
        return PIEZAS.get(random.choice(PIEZAS_KEYS))

    def _getCurrentPiezaColor(self):
        for l in self.current[0]:
            for c in l:
                if c != 0:
                    return c
        return 0

    def _calcularDatosPiezaActual(self):
        m = self.current[self.position[2]]
        coords = []
        for i, l in enumerate(m):
            for j, k in enumerate(l):
                if k != 0:
                    coords.append([i+self.position[0], j+self.position[1]])

        self.currentCoords = coords

    def _esValido(self, x=0, y=0, r=0):
        max_x, max_y = DIM_PLATAFORMA
        if r == 0:
            coordenadas = self.currentCoords
        else:
            m = self.current[(self.position[2]+r) % len(self.current)]
            coords = []
            for i, l in enumerate(m):
                for j, k in enumerate(l):
                    if k != 0:
                        coords.append([i+self.position[0], j+self.position[1]])
            coordenadas = coords

        for cx, cy in coordenadas:
            if not 0 <= x + cx < max_x:
                return False
            elif cy < 0:
                continue
            elif y + cy >= max_y:
                return False
            else:
                if self.plataforma[cy+y][cx+x] != 0:
                    return False
        return True


    def _colocarPieza(self):
        print("La pieza se ha colocado")
        if self.position[1] <= 0:
            self.perdido = True
		# Añadir pieza en la plataforma
        color = self._getCurrentPiezaColor()
        for cx, cy in self.currentCoords:
            self.plataforma[cy][cx] = color
		

        completadas = []
		# calcular las líneas completadas
        for i, line in enumerate(self.plataforma[::-1]):
            for case in line:
                if case == 0:
                    break
            else:
                print(self.plataforma)
                print(">>> %s" % (DIM_PLATAFORMA[1]-1-i))
                completadas.append(DIM_PLATAFORMA[1]-1-i)
        lineas = len(completadas)
        for i in completadas:
            self.plataforma.pop(i)
        for i in range(lineas):
            self.plataforma.insert(0, [0] * DIM_PLATAFORMA[0])
        # calcular la puntuación y otros
        self.lineas += lineas
        self.score += lineas * self.nivel
        self.nivel = int(self.lineas / 10) + 1
        if lineas >= 4:
            self.tetris +=1
            self.score += self.nivel * self.tetris
        # Trabajo con la pieza actual terminado
        self.current = None



    def _first(self):
        self.plataforma = [[0] * DIM_PLATAFORMA[0] for i in range(DIM_PLATAFORMA[1])]
        self.score, self.piezas, self.lineas, self.tetris, self.nivel = 0, 0, 0, 0, 1
        self.current, self.next, self.perdido = None, self._getPieza(), False
        
    def _next(self):
        print("Pieza siguiente")
        self.current, self.next = self.next, self._getPieza()
        self.piezas += 1
        self.position = [int(DIM_PLATAFORMA[0] / 2)-2, -4, 0]
        self._calcularDatosPiezaActual()
        self.ultimo_movimiento = self.ultima_caida = time.time()

    def _gestionarEventos(self):
        event = self._getEvent()
        if event == K_p:
            print("Pausa")
            self.surface.fill(COLORES.get(0))
            self._mostrarTexto('Pausa', CENTRO_VENTANA, font='title')
            self._mostrarTexto('Pulsar una tecla...', POS)
            self._espera()
        elif event == K_LEFT:
            print("Movimiento hacia la izquierda")
            if self._esValido(x=-1):
                self.position[0] -= 1
        elif event == K_RIGHT:
            print("Movimiento hacia la derecha")
            if self._esValido(x=1):
                self.position[0] += 1
        elif event == K_DOWN:
            print("Movimiento hacia abajo")
            if self._esValido(y=1):
                self.position[1] += 1
        elif event == K_UP:
            print("Movimiento de giro")
            if self._esValido(r=1):
                self.position[2] = (self.position[2] + 1) %len(self.current)
        elif event == K_SPACE:
            print("Movimiento de caída %s / %s" % (self.position, self.currentCoords))
            if self.position[1] <=0:
                self.position[1] = 1
                self._calcularDatosPiezaActual()
            a = 0
            while self._esValido(y=a):
                a+=1
            self.position[1] += a-1
        self._calcularDatosPiezaActual()




    def _gestionarGravedad(self):
        if time.time() - self.ultima_caida > GRAVEDAD:
            self.ultima_caida = time.time()
            if not self._esValido():
                print ("Estamos en una posición no válida")
                self.position[1] -= 1
                self._calcularDatosPiezaActual()
                self._colocarPieza()
            elif self._esValido() and not self._esValido(y=1):
                self._calcularDatosPiezaActual()
                self._colocarPieza()
            else:
                print("Se desplaza hacia la parte inferior")
                self.position[1] += 1
                self._calcularDatosPiezaActual()



    def _disenarPlataforma(self):
        self.surface.fill(COLORES.get(0))
        pygame.draw.rect(self.surface, COLORES[8], START_PLABORD+TAMANO_PLABORD, BORDE_PLATAFORMA)
        for i, linea in enumerate(self.plataforma):
            for j, case in enumerate(linea):
                color = COLORES[case]
                position = j, i
                coordenadas = tuple([START_PLATAFORMA[k] + position[k] * TAMANO_BLOQUE[k] for k in range(2)])
                pygame.draw.rect(self.surface, color, coordenadas + TAMANO_BLOQUE)
        if self.current is not None:
            for position in self.currentCoords:
                color = COLORES.get(self._getCurrentPiezaColor())
                coordenadas = tuple([START_PLATAFORMA[k] + position[k] * TAMANO_BLOQUE[k] for k in range(2)])
                pygame.draw.rect(self.surface, color, coordenadas + TAMANO_BLOQUE)
        self.score, self.piezas, self.lineas, self.tetris, self.nivel
        self._mostrarTexto('Score: >%s' % self.score, POSICION_SCORE)
        self._mostrarTexto('Piezas: %s' % self.piezas, POSICION_PIEZAS)
        self._mostrarTexto('Lineas: %s' % self.lineas, POSICION_LINEAS)
        self._mostrarTexto('Tetris: %s' % self.tetris, POSICION_TETRIS)
        self._mostrarTexto('Nivel: %s' % self.nivel, POSICION_NIVEL)

        self._render()



    def play(self):
        print("Partida")
        self.surface.fill(COLORES.get(0))
        self._first()
        while not self.perdido:
            if self.current is None:
                self._next()
            self._gestionarEventos()
            self._gestionarGravedad()
            self._disenarPlataforma()






if __name__ == '__main__':
    juego = Juego()
    juego.start()
    print("Partida empezada")
    juego.play()
    print("Partida terminada")
    juego.stop()
    print("Paro del programa")