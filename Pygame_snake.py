
import sys
import pygame
from pygame.math import Vector2
from random import randint

# Inicializando o Pygame
pygame.init()

# Configurações da tela
fps = pygame.time.Clock()
tamanho = 35
numero = 20
tela = pygame.display.set_mode((numero * tamanho, numero * tamanho))

# Definindo a cor de fundo como uma variável
cor_de_fundo = (140, 170, 30)

# Carregando as imagens e a fonte
pessego_importado = pygame.image.load('emoji.pessego.png').convert_alpha()
tela_inicial = pygame.image.load('tela_inicial.png').convert_alpha()
fonte = pygame.font.Font(None, 70)

# Definindo um evento personalizado para a atualização da tela
ATUALIZACAO_TELA = pygame.USEREVENT
pygame.time.set_timer(ATUALIZACAO_TELA, 150)

# Classe da Cobra
class COBRA:
    def __init__(self):
            self.corpo = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
            self.direcao = Vector2(1,0)
            self.novo_corpo= False
            self.crunch= pygame.mixer.Sound('Som/som-cobra-comendo-pygame.mp3')
            
    def desenhar_cobra(self):
        for bloco in self.corpo: # criando um retangulo 
            pos_x = int(bloco.x * tamanho) # posição x
            pos_y = int(bloco.y * tamanho) # posição y
            bloco_rect = pygame.Rect(pos_x, pos_y, tamanho, tamanho)
            pygame.draw.rect(tela, (83, 0, 210), bloco_rect) # desenhando o retangulo -- cobra 
            # é draw ou desenhar?
    
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

    def toca_som(self):
        self.crunch.play()


# Classe do Pêssego
class PESSEGO:
    def __init__(self):
        self.atualiza_posicao()
    
    def desenhar_pessego(self):
        pessego_rect = pygame.Rect(int(self.pos.x * tamanho), int(self.pos.y * tamanho), tamanho, tamanho)
        tela.blit(pessego_importado, pessego_rect)
    

    def atualiza_posicao(self):
        self.x = randint(0, numero - 1)
        self.y = randint(0, numero - 1)
        
        self.pos = Vector2(self.x, self.y)
    

# Classe do Menu Inicial
class StartMenu:
    def __init__(self):
        self.background = pygame.image.load('tela_inicial.png').convert_alpha()

    def draw(self):
        tela.blit(self.background, (0, 0))

# Classe da tela de Game Over
class GameOverScreen:
    def __init__(self):
        self.game_over_image = pygame.image.load('game_over.png').convert_alpha()
        self.game_over_rect = self.game_over_image.get_rect(center=(numero * tamanho // 2, numero * tamanho // 2))
        self.texto = 0

    def draw(self):
        tela.blit(self.game_over_image, self.game_over_rect)
        self.mensagem(self.texto)

    def mensagem(self, texto):
        mensagem_texto = fonte.render(f"Não foi dessa vez! :(", True, (255, 255, 255))
        mensagem_rect = mensagem_texto.get_rect(center=(numero * tamanho // 2, numero * tamanho // 2 + 50))
        tela.blit(mensagem_texto, mensagem_rect)

# Classe do Jogo Principal
class MAIN:
    def __init__(self):
        self.start_menu = StartMenu()
        self.cobra = COBRA()
        self.pessego = PESSEGO()
        self.game_started = False
        self.game_over = False
        self.game_over_screen = GameOverScreen()

    def start_game(self):
        self.game_started = True

    def update(self):
        if not self.game_started:
            return

        self.cobra.movendo_cobra()
        self.confirma_colisao()
        self.verifica_morte()
    
    def desenha_elementos(self):
        if not self.game_started:
            self.start_menu.draw()
        elif self.game_over:
            self.game_over_screen.draw()
        else:
            self.quadriculado_grama()
            self.pessego.desenhar_pessego()
            self.cobra.desenhar_cobra()
            self.desenha_fonte()

    # cofnirma que a cobra comeu o pessego
    def confirma_colisao(self):
        if self.pessego.pos == self.cobra.corpo[0]:
            # reposiciona a fruta
            self.pessego.atualiza_posicao()
            # adiciona corpo na cobra
            self.cobra.adiciona_corpo()
            # faz  som quando a cobra come
            self.cobra.toca_som()
        # nao permite que a frut seja criada no mesmo lugar em que a cobra ja esta
        for parte in self.cobra.corpo[1:]:
            if parte == self.pessego.pos:
                self.pessego.atualiza_posicao()
        

    def verifica_morte(self):
        if self.game_over:
            return

        # verifica se a cobra bateu na parede
        if not 0 <= self.cobra.corpo[0].x < numero or not 0 <= self.cobra.corpo[0].y < numero:
            self.game_over = True
       
        #verifica se a cobra bateu em seu proprio corpo
        for corpo in self.cobra.corpo[1:]:
            if corpo == self.cobra.corpo[0]:
                self.game_over = True

    def game_over(self):
        self.game_over = True
        self.game_over_screen.pontuacao = len(self.cobra.corpo) - 3
 

    def reiniciar_jogo(self):
        self.cobra = COBRA()
        self.pessego = PESSEGO()
        self.game_started = False
        self.game_over = False


    def quadriculado_grama(self):
        grama_escura = (165, 204, 61)
        for linha in range(numero):
            if linha % 2 == 0:
                for coluna in range(numero):
                    if coluna % 2 == 0:
                        grama = pygame.Rect(coluna * tamanho, linha * tamanho, tamanho, tamanho)
                        pygame.draw.rect(tela, grama_escura, grama)
            else: 
                for coluna in range(numero):
                    if coluna % 2 != 0:
                        grama = pygame.Rect(coluna * tamanho, linha * tamanho, tamanho, tamanho)
                        pygame.draw.rect(tela, grama_escura, grama)

    # pontuacao no canto da tela enquanto o jogo roda
    def desenha_fonte(self):
        pontuacao = str(len(self.cobra.corpo) - 3)
        superfice_texto = fonte.render(pontuacao, True, (60, 75, 10))
        pontuacao_x = int(tamanho * numero - 40)
        pontuacao_y = int(tamanho * numero - 650)
        pontuacao_rect = superfice_texto.get_rect(center=(pontuacao_x, pontuacao_y))
        pessego_rect = pessego_importado.get_rect(midright=(pontuacao_rect.left, pontuacao_rect.centery))
        
        tela.blit(superfice_texto, pontuacao_rect)
        tela.blit(pessego_importado, pessego_rect)


# Criando a instância do jogo principal
jogo_principal = MAIN()

# Loop do jogo
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Iniciando o jogo ao pressionar qualquer tecla
        if not jogo_principal.game_started and evento.type == pygame.KEYDOWN:
            jogo_principal.start_game()

        # Reiniciando o jogo após o Game Over ao pressionar a tecla ENTER
        elif jogo_principal.game_over and evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
            jogo_principal.reiniciar_jogo()

        # Tratamento de teclas para o jogo em andamento
        elif jogo_principal.game_started:
            if evento.type == ATUALIZACAO_TELA:
                jogo_principal.update()
            elif evento.type == pygame.KEYDOWN:
                        #teclas
                        if evento.key == pygame.K_UP:
                            if jogo_principal.cobra.direcao.y != 1:
                                jogo_principal.cobra.direcao = Vector2(0, -1)
                        elif evento.key == pygame.K_RIGHT:
                            if jogo_principal.cobra.direcao.x != -1:
                                jogo_principal.cobra.direcao = Vector2(1, 0)   
                        elif evento.key == pygame.K_DOWN:
                            if jogo_principal.cobra.direcao.y != -1:
                                jogo_principal.cobra.direcao = Vector2(0, 1)
                        elif evento.key == pygame.K_LEFT:
                            if jogo_principal.cobra.direcao.x != 1:
                                jogo_principal.cobra.direcao = Vector2(-1, 0) 

    tela.fill((140, 170, 30))
    jogo_principal.desenha_elementos()

    # Exibe a pontuação na tela de Game Over
    if jogo_principal.game_over:
        jogo_principal.game_over_screen.draw()   
    
    pygame.display.update()
    fps.tick(120)   
