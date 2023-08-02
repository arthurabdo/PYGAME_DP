# inicializacao pygame e outras bibliotecas
import sys
import pygame
from pygame.math import Vector2
from random import randint

# desenahndo a cobra
class COBRA:
    def __init__(self):
        self.corpo = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direcao = Vector2(1,0)
        self.novo_corpo= False
        
    def desenhar_cobra(self):
        for bloco in self.corpo: # criando um retangulo 
            pos_x = int(bloco.x * tamanho) # posição x
            pos_y = int(bloco.y * tamanho) # posição y
            bloco_rect = pygame.Rect(pos_x, pos_y, tamanho, tamanho)
            pygame.draw.rect(tela, (83, 0, 210), bloco_rect) # desenhando o retangulo -- cobra 
            # é draw ou desenhar?

    # movendo a cobra 
    def movendo_cobra (self):
        if self.novo_corpo== True:
            copia_corpo = self.corpo[:] # copiando o corpo adicionando mais um pedaco a ele 
            copia_corpo.insert(0, copia_corpo[0] + self.direcao) # adicionando um novo elemento 
            self.corpo = copia_corpo[:]
            self.novo_corpo= False
        
        else:
            copia_corpo = self.corpo[:-1] # copiando o corpo sem o ultimo bloco
            copia_corpo.insert(0, copia_corpo[0] + self.direcao) # adicionando um novo elemento 
            self.corpo = copia_corpo[:]

    def adiciona_corpo(self):
        self.novo_corpo= True

# desenhando a fruta, que alimenta a cobra e onde ela vai aparecer na tela 
class PESSEGO:
    def __init__(self):
        self.atualiza_posicao()
    
    def desenhar_pessego(self):
        pessego_rect = pygame.Rect(int(self.pos.x * tamanho),int(self.pos.y * tamanho), tamanho, tamanho)
        tela.blit(pessego_importado, pessego_rect)
        # pygame.draw.rect(tela, (250,88,42), pessego_rect)
    

    def atualiza_posicao(self):
        self.x = randint(0, numero - 1)
        self.y = randint(0, numero - 1)
        self.pos = Vector2(self.x, self.y)

#criacao do loop do jogo principal e ajuda a organizacao geral do codigo
class MAIN:
    def __init__(self):
        self.cobra= COBRA()
        self.pessego= PESSEGO()

    def update(self):
        self.cobra.movendo_cobra()
        self.confirma_colisao()
        self.verifica_morte()
    
    def desenha_elementos(self):
        self.pessego.desenhar_pessego()
        self.cobra.desenhar_cobra()

    # cofnirma que a cobra comeu o pessego
    def confirma_colisao(self):
        if self.pessego.pos== self.cobra.corpo[0]:
            # reposiciona a fruta
            self.pessego.atualiza_posicao()
            # adiciona corpo na cobra
            self.cobra.adiciona_corpo()

    def verifica_morte(self):
        # verifica se a cobra bateu na parede
        if not 0<= self.cobra.corpo[0].x < numero or not 0<= self.cobra.corpo[0].y < numero:
            self.game_over()
       
        #verifica se a cobra bateu em seu proprio corpo
        for corpo in self.cobra.corpo[1:]:
            if corpo== self.cobra.corpo[0]:
                self.game_over()


    def game_over(self):
        pygame.quit()
        sys.exit()

pygame.init()
#tela 

fps = pygame.time.Clock()
tamanho = 35
numero = 20
tela = pygame.display.set_mode((numero * tamanho, numero * tamanho))
pessego_importado = pygame.image.load('emoji.pessego.png').convert_alpha()
tela_inicial = pygame.image.load('tela_inicial.png').convert_alpha()

ATUALIZACAO_TELA = pygame.USEREVENT
pygame.time.set_timer(ATUALIZACAO_TELA, 150)

#variavel que se refere ao jogo principal
jogo_principal= MAIN()


# loop do jogo
while True:
    
    for jogo in pygame.event.get():
        if jogo.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if jogo.type == ATUALIZACAO_TELA:
            jogo_principal.update()
        if jogo.type == pygame.KEYDOWN:
            if jogo.key == pygame.K_UP: # para cima 
                # nao deixa a cobra entrar no proprio corpo
                if jogo_principal.cobra.direcao.y != 1:
                    jogo_principal.cobra.direcao = Vector2(0, -1)
            if jogo.key == pygame.K_RIGHT: # para direita
                # nao deixa a cobra entrar no proprio corpo
                if jogo_principal.cobra.direcao.x != -1:
                    jogo_principal.cobra.direcao = Vector2(1, 0)   
            if jogo.key == pygame.K_DOWN: # para baixo 
                # nao deixa a cobra entrar no proprio corpo
                if jogo_principal.cobra.direcao.y != -1:
                    jogo_principal.cobra.direcao = Vector2(0, 1)
            if jogo.key == pygame.K_LEFT: # para esquerda 
                # nao deixa a cobra entrar no proprio corpo
                if jogo_principal.cobra.direcao.x != 1:
                    jogo_principal.cobra.direcao = Vector2(-1, 0) 

    tela.fill((2,15,60))
    jogo_principal.desenha_elementos()
    pygame.display.update()
    fps.tick(120)