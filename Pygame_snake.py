# inicializacao pygame e outras bibliotecas
import sys
import pygame
import random
from pygame.math import Vector2
from random import randint

# desenahndo a cobra
class COBRA:
    def __init__(self):
        self.corpo = [Vector2(5,10), Vector2(6,10), Vector2(7,10)]
        
    def desenhar_cobra(self):
        for bloco in self.corpo: # criando um retangulo 
            pos_x = int(bloco.x * tamanho) # posição x
            pos_y = int(bloco.y * tamanho) # posição y
            bloco_rect = pygame.Rect(pos_x, pos_y, tamanho, tamanho)
            pygame.draw.rect(tela, (230, 230, 250), bloco_rect) # desenhando o retangulo -- cobra 
            # é draw ou desenhar?


# desenhando a fruta, que alimenta a cobra e onde ela vai aparecer na tela 
class PESSEGO:
    def __init__(self):
        self.x = randint(0, numero - 1)
        self.y = randint(0, numero - 1)
        self.pos = Vector2(self.x, self.y)
    
    def desenhar_pessego(self):
        pessego_rect = pygame.Rect(int(self.pos.x * tamanho),int(self.pos.y * tamanho), tamanho, tamanho)
        pygame.draw.rect(tela, (250,88,42), pessego_rect)


pygame.init()
#tela 

fps = pygame.time.Clock()
tamanho = 35
numero = 20
tela = pygame.display.set_mode((numero * tamanho, numero * tamanho))

pessego = PESSEGO()
cobra = COBRA()

# loop do jogo
while True:
    #fechar o jogo
    for jogo in pygame.event.get():
        if jogo.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    tela.fill((2,15,60))
    pessego.desenhar_pessego()
    cobra.desenhar_cobra()
    pygame.display.update()
    fps.tick(120)