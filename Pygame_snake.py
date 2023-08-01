# inicializacao pygame e outras bibliotecas
import sys
import pygame
pygame.init()

#tela 
tela = pygame.display.set_mode((800,600))

# loop do jogo
while True:
    #fechar o jogo
    for jogo in pygame.event.get():
        if jogo.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
