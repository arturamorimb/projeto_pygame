import pygame
import cores
import sys
import random
from pygame.locals import *

def main():
    pygame.init()
    largura, altura = 1000, 600  # Corrigido: largura e altura na ordem correta
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('Cobrathon')
    clock = pygame.time.Clock()

    tam_quadrado = 20
    speed_jogo = 7

    def gerar_comida():
        comida_x = round(random.randrange(0, largura - tam_quadrado) / tam_quadrado) * tam_quadrado
        comida_y = round(random.randrange(0, altura - tam_quadrado) / tam_quadrado) * tam_quadrado
        return comida_x, comida_y

    def draw_comida(tam, comida_x, comida_y):
        pygame.draw.rect(tela, cores.vermelho, [comida_x, comida_y, tam, tam])

    def draw_cobra(tam, pixels):
        for pixel in pixels:
            pygame.draw.rect(tela, cores.verde, [pixel[0], pixel[1], tam, tam])

    def draw_pontos(pontos):
        fonte = pygame.font.SysFont('Gabriola', 40, False, False)
        text = fonte.render(f'Pontos: {pontos}', True, cores.branco)
        tela.blit(text, [1, 1])

    def select_dir(key, dir_x, dir_y):
        # Evita inverter a direção diretamente e suporta WASD e setas
        if (key == pygame.K_DOWN or key == pygame.K_s) and dir_y != -tam_quadrado:
            return 0, tam_quadrado
        elif (key == pygame.K_UP or key == pygame.K_w) and dir_y != tam_quadrado:
            return 0, -tam_quadrado
        elif (key == pygame.K_RIGHT or key == pygame.K_d) and dir_x != -tam_quadrado:
            return tam_quadrado, 0
        elif (key == pygame.K_LEFT or key == pygame.K_a) and dir_x != tam_quadrado:
            return -tam_quadrado, 0
        return dir_x, dir_y

    def rodar_jogo():
        x_cobra = largura / 2
        y_cobra = altura / 2
        dir_xc = 0
        dir_yc = 0
        tam_cobra = 1
        pixels = []
        comida_x, comida_y = gerar_comida()

        while True:
            tela.fill(cores.preto)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    dir_xc, dir_yc = select_dir(event.key, dir_xc, dir_yc)

            x_cobra += dir_xc
            y_cobra += dir_yc

            if x_cobra >= largura:
                x_cobra = 0
            elif x_cobra < 0:
                x_cobra = largura - tam_quadrado
            if y_cobra >= altura:
                y_cobra = 0
            elif y_cobra < 0:
                y_cobra = altura - tam_quadrado

            pixels.append([x_cobra, y_cobra])
            if len(pixels) > tam_cobra:
                del pixels[0]

            for pixel in pixels[:-1]:
                if pixel == [x_cobra, y_cobra]:
                    pygame.quit()
                    sys.exit()

            draw_comida(tam_quadrado, comida_x, comida_y)
            draw_cobra(tam_quadrado, pixels)
            draw_pontos(tam_cobra - 1)

            pygame.display.update()

            if x_cobra == comida_x and y_cobra == comida_y:
                tam_cobra += 1
                comida_x, comida_y = gerar_comida()

            clock.tick(speed_jogo)

    rodar_jogo()

if __name__ == '__main__':
    main()
