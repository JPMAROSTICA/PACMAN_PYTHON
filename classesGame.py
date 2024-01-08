import pygame
import random
import os
import time

pygame.font.init()

class Settings:
    #CONFIGURAÇÕES GERAIS
    TELA_ALTURA, TELA_LARGURA = 510, 1380
    TELA = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    RELOGIO = pygame.time.Clock()
    VELOCIDADE_JOGO = 8

    #CORES
    PRETA = (0,0,0)
    BRANCA = (255,255,255)
    VERMELHA = (255,0,0)
    AMARELO = (128,128,0)
    AZUL = (0,0,255)
    VERDE_ESCURO = (0,128,0)

    COR_BARREIRA = AZUL

    TAMANHO = (30,30)
    VELOCIDADE_PACMAN = 30
    VELOCIDADE_GHOST = 30

    SCALE = (35,35)
    SCALE2 = (50,50)

    FASE = 1
    SCORE_ACUMULADO = 0

    #IMAGENS
    GHOST_AZUL = [pygame.transform.scale(pygame.image.load(os.path.join('Imagens', 'ghost azul direita.png')),SCALE),
                  pygame.transform.scale(pygame.image.load(os.path.join('Imagens', 'ghost azul frente.png')),SCALE),
                  pygame.transform.scale(pygame.image.load(os.path.join('Imagens', 'ghost azul.png')),SCALE)]

    GHOST_AMARELO = [pygame.transform.scale(pygame.image.load(os.path.join('Imagens', 'ghost amarelo esquerda.png')),SCALE),
                     pygame.transform.scale(pygame.image.load(os.path.join('Imagens', 'ghost amarelo frentee.png')),SCALE),
                     pygame.transform.scale(pygame.image.load(os.path.join('Imagens', 'ghost amarelo.png')),SCALE)]

    GHOST_VERMELHO = [pygame.transform.scale(pygame.image.load(os.path.join('Imagens', 'ghost vermelho direita.png')),SCALE),
                      pygame.transform.scale(pygame.image.load(os.path.join('Imagens', 'ghost vermelho frente.png')),SCALE),
                      pygame.transform.scale(pygame.image.load(os.path.join('Imagens', 'ghost vermelho.png')),SCALE)]

    OLHOS_GHOST = [pygame.transform.scale(pygame.image.load(os.path.join('Imagens', 'olhos para direita.png')),SCALE2),
                   pygame.transform.scale(pygame.image.load(os.path.join('Imagens', 'olhos para esquerda.png')),SCALE2),
                   pygame.transform.scale(pygame.image.load(os.path.join('Imagens', 'olhos para frente.png')),SCALE2)]

    PAC_MAN = [pygame.transform.scale(pygame.image.load(os.path.join('Imagens', 'pack_fechado.png')),SCALE),
               pygame.transform.scale(pygame.image.load(os.path.join('Imagens', 'pack_aberto1.png')),SCALE),
               pygame.transform.scale(pygame.image.load(os.path.join('Imagens', 'pack_aberto2.png')),SCALE),
               pygame.transform.scale(pygame.image.load(os.path.join('Imagens', 'pack_fechadoCima.png')),SCALE),
               pygame.transform.scale(pygame.image.load(os.path.join('Imagens', 'pack_aberto1Cima.png')),SCALE),
               pygame.transform.scale(pygame.image.load(os.path.join('Imagens', 'pack_aberto2Cima.png')),SCALE)]

    PAC_MAN_MORRENDO = [pygame.transform.scale(pygame.image.load(os.path.join('Imagens', 'pacDesfazenfo1.png')),SCALE),
                        pygame.transform.scale(pygame.image.load(os.path.join('Imagens', 'pacDesfazenfo2.png')),SCALE),
                        pygame.transform.scale(pygame.image.load(os.path.join('Imagens', 'pacDesfazenfo3.png')),SCALE),
                        pygame.transform.scale(pygame.image.load(os.path.join('Imagens', 'pacDesfazenfo4.png')),SCALE),
                        pygame.transform.scale(pygame.image.load(os.path.join('Imagens', 'pacDesfazenfo5.png')),SCALE),
                        pygame.transform.scale(pygame.image.load(os.path.join('Imagens', 'pacDesfazenfo6.png')),SCALE)]

    FOOD = [pygame.image.load(os.path.join('Imagens', 'food1.png')),
            pygame.image.load(os.path.join('Imagens', 'food2.png')),
            pygame.image.load(os.path.join('Imagens', 'food3.png'))]

    ENERGIA = [pygame.image.load(os.path.join('Imagens', 'energia1.png')),
               pygame.image.load(os.path.join('Imagens', 'energia2.png')),
               pygame.image.load(os.path.join('Imagens', 'energia3.png'))]

    APPLE = [pygame.image.load(os.path.join('Imagens', 'apple1.png')),
             pygame.image.load(os.path.join('Imagens', 'apple2.png')),
             pygame.image.load(os.path.join('Imagens', 'apple3.png'))]

    FONTE = pygame.font.SysFont("Helvetica", 15)
    FONTE_SCORE = pygame.font.SysFont("Comic Sans MS", 25, "bold")
    FONTE_READY = pygame.font.SysFont("Comic Sans MS", 45, "bold")

class Animation:
    def __init__(self):
        self.contadorGhost = 0
        self.limite_contagem_ghost = 1

    def animation(self,imagem):
        imag = imagem[0]
        if self.contadorGhost >=0 and self.contadorGhost<self.limite_contagem_ghost: imag = imagem[0]
        elif self.contadorGhost>=self.limite_contagem_ghost and self.contadorGhost<2*self.limite_contagem_ghost: imag = imagem[1]
        elif self.contadorGhost>=2*self.limite_contagem_ghost and self.contadorGhost<3*self.limite_contagem_ghost: imag = imagem[2]
        elif self.contadorGhost>=3*self.limite_contagem_ghost and self.contadorGhost<4*self.limite_contagem_ghost: imag = imagem[1]
        elif self.contadorGhost >= 4*self.limite_contagem_ghost: self.contadorGhost = 0

        self.contadorGhost += 1

        return imag

class Sprites:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.moveRight = False
        self.moveLeft = False
        self.moveUp = False
        self.moveDown = False
        self.lookingRight = False
        self.lookingLeft = False
        self.lookingDown = False
        self.lookingUp = False
        self.colider = pygame.Rect(self.x,self.y,Settings.TAMANHO[0],Settings.TAMANHO[1])

    def adiantarEntradaNaPassagemComUmaCasaDeResponsividade(self,right,left,up,down,barreira):
        #Este método serve para reposicionar o pacMan sempre que o player apertar uma tecla para mudar sua direção estando posicionado uma casa antes d aabertura
        #Para melhorar a jogabilidade, verificaremos se existe uma abertura na posção posterior à do pacMan, se houver o transportaremos para lá

        rectColiderGenerico = ''

        #Por exemplo, se o player clicar para a direita e ele estiver naquele momento se movendo para cima, criaremos um objeto rect acima e a direita do pacMan
        #Se naquela posição não houver uma barreira, o pacMan assumirá aquela posição
        #Por esse motivo, os métodos lookingUp,lookingDown,lookingRight,lookingLeft são atualizados somente após a consumação da mudança de direção
        if right:
            if self.lookingUp: rectColiderGenerico = pygame.Rect(self.x+Settings.TAMANHO[0],self.y-Settings.TAMANHO[1],Settings.TAMANHO[0],Settings.TAMANHO[1])
            elif self.lookingDown: rectColiderGenerico = pygame.Rect(self.x+Settings.TAMANHO[0],self.y+Settings.TAMANHO[1],Settings.TAMANHO[0],Settings.TAMANHO[1])
        if left:
            if self.lookingUp: rectColiderGenerico = pygame.Rect(self.x-Settings.TAMANHO[0],self.y-Settings.TAMANHO[1],Settings.TAMANHO[0],Settings.TAMANHO[1])
            elif self.lookingDown: rectColiderGenerico = pygame.Rect(self.x-Settings.TAMANHO[0],self.y+Settings.TAMANHO[1],Settings.TAMANHO[0],Settings.TAMANHO[1])
        if up:
            if self.lookingRight: rectColiderGenerico = pygame.Rect(self.x+Settings.TAMANHO[0],self.y-Settings.TAMANHO[1],Settings.TAMANHO[0],Settings.TAMANHO[1])
            elif self.lookingLeft: rectColiderGenerico = pygame.Rect(self.x-Settings.TAMANHO[0],self.y-Settings.TAMANHO[1],Settings.TAMANHO[0],Settings.TAMANHO[1])
        if down:
            if self.lookingRight: rectColiderGenerico = pygame.Rect(self.x+Settings.TAMANHO[0],self.y+Settings.TAMANHO[1],Settings.TAMANHO[0],Settings.TAMANHO[1])
            elif self.lookingLeft: rectColiderGenerico = pygame.Rect(self.x-Settings.TAMANHO[0],self.y+Settings.TAMANHO[1],Settings.TAMANHO[0],Settings.TAMANHO[1])


        if rectColiderGenerico != '':
            if not rectColiderGenerico in barreira: self.x,self.y = rectColiderGenerico.x,rectColiderGenerico.y

    def mover(self,barreira,velocidade):
        #O PACMAN SÓ VAI SE MOVER PARA UMA DETERMINADA DIREÇÃO SE NÃO HOUVER UMA BARREIRA A SUA FRENTE
        #O GHOST SE MOVE PELSO SENSORES, ENTÃO NÃO PRECISAMOS VERIFICAR MAIS NADA, SOMENTE ALTERAR SUA POSIÇÃO
        if self.moveRight:
            rectColiderGenerico = pygame.Rect(self.x+Settings.TAMANHO[0],self.y,Settings.TAMANHO[0],Settings.TAMANHO[1])
            if type(self) is not Ghost:
                if not rectColiderGenerico in barreira: self.x += velocidade
                else: self.adiantarEntradaNaPassagemComUmaCasaDeResponsividade(True,False,False,False,barreira)
            else: self.x += velocidade

            #atualizamos o status após consumar a direção
            self.lookingRight,self.lookingLeft,self.lookingUp,self.lookingDown = True,False,False,False

        if self.moveLeft:
            rectColiderGenerico = pygame.Rect(self.x-Settings.TAMANHO[0],self.y,Settings.TAMANHO[0],Settings.TAMANHO[1])
            if type(self) is not Ghost:
                if not rectColiderGenerico in barreira: self.x -= velocidade
                else: self.adiantarEntradaNaPassagemComUmaCasaDeResponsividade(False,True,False,False,barreira)
            else: self.x -= velocidade

            #atualizamos o status após consumar a direção
            self.lookingRight,self.lookingLeft,self.lookingUp,self.lookingDown = False,True,False,False

        if self.moveUp:
            rectColiderGenerico = pygame.Rect(self.x,self.y-Settings.TAMANHO[1],Settings.TAMANHO[0],Settings.TAMANHO[1])
            if type(self) is not Ghost:
                if not rectColiderGenerico in barreira: self.y -= velocidade
                else: self.adiantarEntradaNaPassagemComUmaCasaDeResponsividade(False,False,True,False,barreira)
            else: self.y -= velocidade

            #atualizamos o status após consumar a direção
            self.lookingRight,self.lookingLeft,self.lookingUp,self.lookingDown = False,False,True,False

        if self.moveDown:
            rectColiderGenerico = pygame.Rect(self.x,self.y+Settings.TAMANHO[1],Settings.TAMANHO[0],Settings.TAMANHO[1])
            if type(self) is not Ghost:
                if not rectColiderGenerico in barreira: self.y += velocidade
                else: self.adiantarEntradaNaPassagemComUmaCasaDeResponsividade(False,False,False,True,barreira)
            else: self.y += velocidade

            #atualizamos o status após consumar a direção
            self.lookingRight,self.lookingLeft,self.lookingUp,self.lookingDown = False,False,False,True

class pacMan(Sprites):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.hp = 100
        self.score = 0
        self.velocidade = Settings.VELOCIDADE_PACMAN
        self.imagem = Settings.PAC_MAN[0]
        self.imagens = []
        for i in range(0,3,1): self.imagens.append(Settings.PAC_MAN[i])
        self.animation = Animation()


    def desenhar(self,game):
        if not game.isGameOver:
            if self.moveRight:
                self.imagens = []
                for i in range(0,3,1): self.imagens.append(Settings.PAC_MAN[i])
            if self.moveLeft:
                self.imagens = []
                for i in range(0,3,1): self.imagens.append(pygame.transform.flip(Settings.PAC_MAN[i],True,False))
            if self.moveUp:
                self.imagens = []
                for i in range(3,6,1): self.imagens.append(Settings.PAC_MAN[i])
            if self.moveDown:
                self.imagens = []
                for i in range(3,6,1): self.imagens.append(pygame.transform.flip(Settings.PAC_MAN[i],False,True))

            self.imagem = self.animation.animation(self.imagens)

        Settings.TELA.blit(self.imagem, (self.x, self.y))

    def verificarSeObjetosForamCapturados(self,objetosNoCenario):
        return list(filter(lambda objetoCenario: objetoCenario.colider == self.colider,objetosNoCenario))

    def alterarOsAtributosAposACapturaDeObjetosNoCenario(self,objetosCapturados):
        for each_objeto in objetosCapturados:
            self.hp += each_objeto.hp
            if self.hp > 100: self.hp = 100

            self.score += each_objeto.score

class Ghost(Sprites):
    def __init__(self,x,y,imagem):
        super().__init__(x,y)
        self.states = {
            1: 'Attacker', #Status em que o ghost pode atacar
            2: 'Atacked', #Status em que o ghost pode ser atacado, quando o pacMan comer a célula de energia
            3: 'Recovering', #Status em que o ghost segue na direção para sua recuperação
            4: 'Breeding' #Status inicial do ghost, assim que ele sai de sua casa pela primeira vez
        }

        self.state = self.states[4]
        self.velocidade = Settings.VELOCIDADE_GHOST
        self.imagens = imagem
        self.imagem = self.imagens[0]
        self.contadorDeTempoDeContatoComOPacMan = 0
        self.animation = Animation()
        self.scoreParaOPAcMan = 200
        self.pacManJaGanhouScoreSobreMim = False
        self.contadorDeTempoDaMensagemDePontuacaoQuandoOPacManComeOGhost = 0

    def desenhar(self):
        if self.state == 'Attacker': self.imagem = self.animation.animation(self.imagens)
        if self.state == 'Atacked': self.imagem = self.animation.animation(Settings.GHOST_AZUL)
        if self.state == 'Recovering': cor = self.imagem = self.animation.animation(Settings.OLHOS_GHOST)

        Settings.TELA.blit(self.imagem, (self.x, self.y))

    def definirPossiveisDirecoesAPartirDeUmPontoDeSensor(self,sensores):
        possiveisDirecoes = []
        for each_sensor in sensores:
            if each_sensor.colider == self.colider:
                sensor = sensores[sensores.index(each_sensor)]
                if sensor.canMoveRight: possiveisDirecoes.append('Right')
                if sensor.canMoveLeft: possiveisDirecoes.append('Left')
                if sensor.canMoveUp: possiveisDirecoes.append('Up')
                if sensor.canMoveDown: possiveisDirecoes.append('Down')

                #caso o ghost esteja em estado de Recovering, ele poderá acessar sua 'casa'. Esses dois sensores aqui tratados, não darão acesso diretoa casa
                #Porém, quando o ghost estiver em estado de 'Recovering', ele deverá entrar direto na casa quando encontrá-la
                if self.state == 'Recovering':
                    if each_sensor.colider == pygame.Rect(600,210,Settings.TAMANHO[0],Settings.TAMANHO[1]): #Sensores(600,210,False,True,True,True):
                        possiveisDirecoes.clear()
                        possiveisDirecoes.append('Right')

                    if each_sensor.colider == pygame.Rect(780,210,Settings.TAMANHO[0],Settings.TAMANHO[1]): #Sensores(780,210,True,False,True,True):
                        possiveisDirecoes.clear()
                        possiveisDirecoes.append('Left')
                break

        return possiveisDirecoes

    def definirDistanciasDoPontoDeReferencia(self,possiveisDirecoes,coliderDeReferencia):
        listaDeDistanciasDoPontoDereferencia = []
        if 'Right' in possiveisDirecoes:
            rectGenerico = pygame.Rect(self.x+60,self.y,Settings.TAMANHO[0],Settings.TAMANHO[1])
            distancia = ((rectGenerico.x-coliderDeReferencia.x)**2 + (rectGenerico.y-coliderDeReferencia.y)**2)**(1/2)
            listaDeDistanciasDoPontoDereferencia.append((distancia,'Right'))

        if 'Left' in possiveisDirecoes:
            rectGenerico = pygame.Rect(self.x-60,self.y,Settings.TAMANHO[0],Settings.TAMANHO[1])
            distancia = ((rectGenerico.x-coliderDeReferencia.x)**2 + (rectGenerico.y-coliderDeReferencia.y)**2)**(1/2)
            listaDeDistanciasDoPontoDereferencia.append((distancia,'Left'))

        if 'Up' in possiveisDirecoes:
            rectGenerico = pygame.Rect(self.x,self.y-60,Settings.TAMANHO[0],Settings.TAMANHO[1])
            distancia = ((rectGenerico.x-coliderDeReferencia.x)**2 + (rectGenerico.y-coliderDeReferencia.y)**2)**(1/2)
            listaDeDistanciasDoPontoDereferencia.append((distancia,'Up'))

        if 'Down' in possiveisDirecoes:
            rectGenerico = pygame.Rect(self.x,self.y+60,Settings.TAMANHO[0],Settings.TAMANHO[1])
            distancia = ((rectGenerico.x-coliderDeReferencia.x)**2 + (rectGenerico.y-coliderDeReferencia.y)**2)**(1/2)
            listaDeDistanciasDoPontoDereferencia.append((distancia,'Down'))
        return listaDeDistanciasDoPontoDereferencia

    def consumarADirecao(self,listaDeDistanciasDoPontoDereferencia):
        if listaDeDistanciasDoPontoDereferencia[0][1] == 'Right': self.moveRight,self.moveLeft,self.moveUp,self.moveDown = True,False,False,False
        if listaDeDistanciasDoPontoDereferencia[0][1] == 'Left': self.moveRight,self.moveLeft,self.moveUp,self.moveDown = False,True,False,False
        if listaDeDistanciasDoPontoDereferencia[0][1] == 'Up': self.moveRight,self.moveLeft,self.moveUp,self.moveDown = False,False,True,False
        if listaDeDistanciasDoPontoDereferencia[0][1] == 'Down': self.moveRight,self.moveLeft,self.moveUp,self.moveDown = False,False,False,True

    def definirMelhorDirecaoParaseguirPacMan(self,listaDeDistanciasDoPontoDereferencia,gerenciadorDeObjetos):
        listaDeDistanciasDoPontoDereferencia = gerenciadorDeObjetos.ordenarListaDeTuplasEmOrdemCrescente(listaDeDistanciasDoPontoDereferencia)
        self.consumarADirecao(listaDeDistanciasDoPontoDereferencia)

    def definirMelhorDirecaoParaSeAfastarDoPacMan(self,listaDeDistanciasDoPontoDereferencia,gerenciadorDeObjetos):
        listaDeDistanciasDoPontoDereferencia = gerenciadorDeObjetos.ordenarListaDeTuplasEmOrdemDecrescente(listaDeDistanciasDoPontoDereferencia)
        self.consumarADirecao(listaDeDistanciasDoPontoDereferencia)

    #sei que os métodos definirMelhorDirecaoParaseguirPacMan, definirMelhorDirecaoParaSeAfastarDoPacMan e definirDirecaoParaVoltarParaCasa
    #são identicos. Perderemos no reaproveitamento de código aqui para facilitar a leitura do que está acontecendo durante as chamadas dos métodos no movimento do ghost
    def definirDirecaoParaVoltarParaCasa(self,listaDeDistanciasDoPontoDereferencia,gerenciadorDeObjetos):
        listaDeDistanciasDoPontoDereferencia = gerenciadorDeObjetos.ordenarListaDeTuplasEmOrdemCrescente(listaDeDistanciasDoPontoDereferencia)
        self.consumarADirecao(listaDeDistanciasDoPontoDereferencia)

    def seSepararDeGhostsQueCruzamNoMesmoPonto(self,allGhosts,barreiras):
        #AQUI VAMOS PROCURAR POR GHOSTS QUE ACABAM SE ENCONTRANDO COM OUTROS GHOSTS NO MESMO PONTO
        #SE ISSO ACONTECER VAMOS DETERMINAR A SEPARAÇÃO DOS GHOSTS. COLOCAMOS UM CONTADOR PARA QUE ESSA SEPARAÇÃO NÃO ACONTEÇA EM QUALQUER COLISÃO
        #QUEREMOS QUE OS GHOSTS SE SEPAREM SOMENTE QUANDO ELES SEGUIREM JUNTOS POR UM CERTO TEMPO
        direcoesPossiveisParaSeguir = []
        if Settings.VELOCIDADE_GHOST == 30:
            for each_ghost in allGhosts:
                if not each_ghost == self:
                    if each_ghost.colider == self.colider:

                        #Se o ghost tiver que se separar, determinamos para qual direção ele pode seguir sem que ele colida com uma barreira
                        #Para isso, pegamos um rect generico para cada uma das duas direções, e quatro sentidos, depois filtramos aqueles que não colidem com nenhuma barreira
                        right = pygame.Rect(self.x+30,self.y,Settings.TAMANHO[0],Settings.TAMANHO[1])
                        left = pygame.Rect(self.x-30,self.y,Settings.TAMANHO[0],Settings.TAMANHO[1])
                        up = pygame.Rect(self.x,self.y-30,Settings.TAMANHO[0],Settings.TAMANHO[1])
                        down = pygame.Rect(self.x,self.y+30,Settings.TAMANHO[0],Settings.TAMANHO[1])

                        direcoesPossiveisParaSeguir = [(right,'Right'),(left,'Left'),(up,'Up'),(down,'Down')]
                        direcoesPossiveisParaSeguir = list(filter(lambda direcoes: direcoes[0] not in barreiras,direcoesPossiveisParaSeguir))

                        #Escolhemos aleatoriamente uma direção para seguir a partir das direções possíveis
                        indice = random.randrange(0,len(direcoesPossiveisParaSeguir))
                        if direcoesPossiveisParaSeguir[indice][1] == 'Right': self.moveRight,self.moveLeft,self.moveUp,self.moveDown = True,False,False,False
                        if direcoesPossiveisParaSeguir[indice][1] == 'Left': self.moveRight,self.moveLeft,self.moveUp,self.moveDown = False,True,False,False
                        if direcoesPossiveisParaSeguir[indice][1] == 'Up': self.moveRight,self.moveLeft,self.moveUp,self.moveDown = False,False,True,False
                        if direcoesPossiveisParaSeguir[indice][1] == 'Down': self.moveRight,self.moveLeft,self.moveUp,self.moveDown = False,False,False,True

    def colideWithPacManAsAnAttacker(self,pacMan):
        colisao = pygame.Rect.colliderect(pacMan.colider,self.colider)
        #aqui evitamos que o ghost dê danos continuos se ele seguir um tempo grudado com o pacMan
        if colisao:
            if self.contadorDeTempoDeContatoComOPacMan == 0: pacMan.hp -= 10

            self.contadorDeTempoDeContatoComOPacMan += 1
            #depois de um tempo grudado, zeramos o contador novamente
            if self.contadorDeTempoDeContatoComOPacMan >= 20: self.contadorDeTempoDeContatoComOPacMan = 0
        else: self.contadorDeTempoDeContatoComOPacMan = 0

        if pacMan.hp <= 0: pacMan.hp = 0

    def colideWithPacManAsAnAttacked(self,pacMan):
        colisao = pygame.Rect.colliderect(pacMan.colider,self.colider)
        if colisao: self.state = self.states[3]

        #esse caso garante a colisão quando o pacMan e Ghost passam um pelo outro após ambos andarem 30 pixels para direções opostas,
        #o que pode fazer com que seus coliders não se sobreponham diretamente
        else:
            for i in range(-30,30,5):
                colider = pygame.Rect(self.colider.x+i,self.colider.y,Settings.TAMANHO[0],Settings.TAMANHO[1])
                colisao = pygame.Rect.colliderect(pacMan.colider,colider)
                if colisao:
                    self.state = self.states[3]
                    break

                colider = pygame.Rect(self.colider.x,self.colider.y+i,Settings.TAMANHO[0],Settings.TAMANHO[1])
                colisao = pygame.Rect.colliderect(pacMan.colider,colider)
                if colisao:
                    self.state = self.states[3]
                    break

    def voltarASerAtackerDepoisDoRecover(self):
        retanguloDosSensoresDaCasaDoGhost = [pygame.Rect(660,210,Settings.TAMANHO[0],Settings.TAMANHO[1]),pygame.Rect(720,210,Settings.TAMANHO[0],Settings.TAMANHO[1])]
        if self.colider in retanguloDosSensoresDaCasaDoGhost:
            self.state = self.states[1]
            self.pacManJaGanhouScoreSobreMim = False
            self.contadorDeTempoDaMensagemDePontuacaoQuandoOPacManComeOGhost = 0

#Essa classe instanciará os 'sensores' do jogo. Serão retângulos espalhados pelo cenário para determinar as direções que os ghosts podem seguir
#Sempre que um ghost colidir com um sensor, ele terá que tomar uma decisão e escolher uma direção possível
class Sensores:
    def __init__(self,x,y,right,left,up,down):
        self.x = x
        self.y = y
        self.canMoveRight = right
        self.canMoveLeft = left
        self.canMoveUp = up
        self.canMoveDown = down
        self.colider = pygame.Rect(self.x,self.y,Settings.TAMANHO[0],Settings.TAMANHO[0])

    def desenhar(self):
        pygame.draw.rect(Settings.TELA,Settings.BRANCA,[self.colider.x,self.colider.y,self.colider.width,self.colider.height])

class Barreiras:
    def __init__(self):
        self.barreiras = []

    def definirBarreirasCanto(self):
        for i in range(0,Settings.TELA_ALTURA+Settings.TAMANHO[1],Settings.TAMANHO[1]):
            self.barreiras.append(pygame.Rect(0,i,Settings.TAMANHO[0],Settings.TAMANHO[1]))
            self.barreiras.append(pygame.Rect(Settings.TELA_LARGURA-Settings.TAMANHO[1],i,Settings.TAMANHO[0],Settings.TAMANHO[1]))

        for i in range(Settings.TAMANHO[0],Settings.TELA_LARGURA,Settings.TAMANHO[0]):
            self.barreiras.append(pygame.Rect(i,0,Settings.TAMANHO[0],Settings.TAMANHO[1]))
            self.barreiras.append(pygame.Rect(i,Settings.TELA_ALTURA-Settings.TAMANHO[0],Settings.TAMANHO[0],Settings.TAMANHO[1]))

    def definirBarreirasCentrais(self):
        for i in range(630,780,30): self.barreiras.append(pygame.Rect(i,60,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(630,780,30): self.barreiras.append(pygame.Rect(i,120,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(630,780,30): self.barreiras.append(pygame.Rect(i,180,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(630,780,30): self.barreiras.append(pygame.Rect(i,300,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(630,780,30): self.barreiras.append(pygame.Rect(i,360,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(630,780,30): self.barreiras.append(pygame.Rect(i,420,Settings.TAMANHO[0],Settings.TAMANHO[1]))

        for i in range(210,300,30): self.barreiras.append(pygame.Rect(630,i,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(210,300,30): self.barreiras.append(pygame.Rect(750,i,Settings.TAMANHO[0],Settings.TAMANHO[1]))

    def definirBarreirasFase1(self):
        #HORIZONTAIS
        for i in range(60,300,30): self.barreiras.append(pygame.Rect(i,60,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(30,180,30): self.barreiras.append(pygame.Rect(i,120,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(210,360,30): self.barreiras.append(pygame.Rect(i,120,Settings.TAMANHO[0],Settings.TAMANHO[1]))

        for i in range(60,300,30): self.barreiras.append(pygame.Rect(i,180,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(30,180,30): self.barreiras.append(pygame.Rect(i,240,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(210,360,30): self.barreiras.append(pygame.Rect(i,240,Settings.TAMANHO[0],Settings.TAMANHO[1]))

        for i in range(60,300,30): self.barreiras.append(pygame.Rect(i,300,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(30,180,30): self.barreiras.append(pygame.Rect(i,360,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(210,360,30): self.barreiras.append(pygame.Rect(i,360,Settings.TAMANHO[0],Settings.TAMANHO[1]))

        for i in range(60,300,30): self.barreiras.append(pygame.Rect(i,420,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(30,180,30): self.barreiras.append(pygame.Rect(i,480,Settings.TAMANHO[0],Settings.TAMANHO[1]))

        for i in range(390,540,30): self.barreiras.append(pygame.Rect(i,60,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(390,600,30): self.barreiras.append(pygame.Rect(i,120,Settings.TAMANHO[0],Settings.TAMANHO[1]))

        for i in range(390,540,30): self.barreiras.append(pygame.Rect(i,180,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(390,600,30): self.barreiras.append(pygame.Rect(i,240,Settings.TAMANHO[0],Settings.TAMANHO[1]))

        for i in range(390,540,30): self.barreiras.append(pygame.Rect(i,300,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(390,600,30): self.barreiras.append(pygame.Rect(i,360,Settings.TAMANHO[0],Settings.TAMANHO[1]))

        for i in range(390,540,30): self.barreiras.append(pygame.Rect(i,420,Settings.TAMANHO[0],Settings.TAMANHO[1]))

        #VERTICAIS
        for i in range(60,120,30): self.barreiras.append(pygame.Rect(330,i,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(150,210,30): self.barreiras.append(pygame.Rect(330,i,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(300,360,30): self.barreiras.append(pygame.Rect(330,i,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(420,480,30): self.barreiras.append(pygame.Rect(330,i,Settings.TAMANHO[0],Settings.TAMANHO[1]))

        for i in range(30,90,30): self.barreiras.append(pygame.Rect(570,i,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(150,210,30): self.barreiras.append(pygame.Rect(570,i,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(150,210,30): self.barreiras.append(pygame.Rect(570,i,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(270,330,30): self.barreiras.append(pygame.Rect(570,i,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(390,450,30): self.barreiras.append(pygame.Rect(570,i,Settings.TAMANHO[0],Settings.TAMANHO[1]))

        for i in range(60,300,30): self.barreiras.append(pygame.Rect(i,60,Settings.TAMANHO[0],Settings.TAMANHO[1]))

        for i in range(30,90,30): self.barreiras.append(pygame.Rect(810,i,Settings.TAMANHO[0],Settings.TAMANHO[1]))


        #HORIZONTAIS ESPELHADOS
        for i in range(Settings.TELA_LARGURA-90,Settings.TELA_LARGURA-300,-30): self.barreiras.append(pygame.Rect(i,60,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(Settings.TELA_LARGURA-60,Settings.TELA_LARGURA-180,-30): self.barreiras.append(pygame.Rect(i,120,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(Settings.TELA_LARGURA-210,Settings.TELA_LARGURA-360,-30): self.barreiras.append(pygame.Rect(i,120,Settings.TAMANHO[0],Settings.TAMANHO[1]))

        for i in range(Settings.TELA_LARGURA-90,Settings.TELA_LARGURA-300,-30): self.barreiras.append(pygame.Rect(i,180,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(Settings.TELA_LARGURA-60,Settings.TELA_LARGURA-180,-30): self.barreiras.append(pygame.Rect(i,240,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(Settings.TELA_LARGURA-210,Settings.TELA_LARGURA-360,-30): self.barreiras.append(pygame.Rect(i,240,Settings.TAMANHO[0],Settings.TAMANHO[1]))

        for i in range(Settings.TELA_LARGURA-90,Settings.TELA_LARGURA-300,-30): self.barreiras.append(pygame.Rect(i,300,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(Settings.TELA_LARGURA-60,Settings.TELA_LARGURA-180,-30): self.barreiras.append(pygame.Rect(i,360,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(Settings.TELA_LARGURA-210,Settings.TELA_LARGURA-360,-30): self.barreiras.append(pygame.Rect(i,360,Settings.TAMANHO[0],Settings.TAMANHO[1]))

        for i in range(Settings.TELA_LARGURA-90,Settings.TELA_LARGURA-300,-30): self.barreiras.append(pygame.Rect(i,420,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(Settings.TELA_LARGURA-60,Settings.TELA_LARGURA-180,-30): self.barreiras.append(pygame.Rect(i,480,Settings.TAMANHO[0],Settings.TAMANHO[1]))

        for i in range(Settings.TELA_LARGURA-390,Settings.TELA_LARGURA-540,-30): self.barreiras.append(pygame.Rect(i,60,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(Settings.TELA_LARGURA-390,Settings.TELA_LARGURA-600,-30): self.barreiras.append(pygame.Rect(i,120,Settings.TAMANHO[0],Settings.TAMANHO[1]))

        for i in range(Settings.TELA_LARGURA-390,Settings.TELA_LARGURA-540,-30): self.barreiras.append(pygame.Rect(i,180,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(Settings.TELA_LARGURA-390,Settings.TELA_LARGURA-600,-30): self.barreiras.append(pygame.Rect(i,240,Settings.TAMANHO[0],Settings.TAMANHO[1]))

        for i in range(Settings.TELA_LARGURA-390,Settings.TELA_LARGURA-540,-30): self.barreiras.append(pygame.Rect(i,300,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(Settings.TELA_LARGURA-390,Settings.TELA_LARGURA-600,-30): self.barreiras.append(pygame.Rect(i,360,Settings.TAMANHO[0],Settings.TAMANHO[1]))

        for i in range(Settings.TELA_LARGURA-390,Settings.TELA_LARGURA-540,-30): self.barreiras.append(pygame.Rect(i,420,Settings.TAMANHO[0],Settings.TAMANHO[1]))

        #VERTICAIS ESPELHADOS
        for i in range(60,120,30): self.barreiras.append(pygame.Rect(Settings.TELA_LARGURA-330,i,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(150,210,30): self.barreiras.append(pygame.Rect(Settings.TELA_LARGURA-330,i,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(300,360,30): self.barreiras.append(pygame.Rect(Settings.TELA_LARGURA-330,i,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(420,480,30): self.barreiras.append(pygame.Rect(Settings.TELA_LARGURA-330,i,Settings.TAMANHO[0],Settings.TAMANHO[1]))

        for i in range(30,90,30): self.barreiras.append(pygame.Rect(Settings.TELA_LARGURA-570,i,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(150,210,30): self.barreiras.append(pygame.Rect(Settings.TELA_LARGURA-570,i,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(150,210,30): self.barreiras.append(pygame.Rect(Settings.TELA_LARGURA-570,i,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(270,330,30): self.barreiras.append(pygame.Rect(Settings.TELA_LARGURA-570,i,Settings.TAMANHO[0],Settings.TAMANHO[1]))
        for i in range(390,450,30): self.barreiras.append(pygame.Rect(Settings.TELA_LARGURA-570,i,Settings.TAMANHO[0],Settings.TAMANHO[1]))


    def desenhar(self):
        for each_barreira in self.barreiras:
            pygame.draw.rect(Settings.TELA,Settings.COR_BARREIRA,[each_barreira.x,each_barreira.y,Settings.TAMANHO[0],Settings.TAMANHO[1]],2,8)

class objetosCapturaveis:
    def __init__(self,x,y,tipo):
        self.x = x
        self.y = y
        if tipo == 'comida':
            self.hp = 0
            self.score = 50
            self.imagem = Settings.FOOD
        elif tipo == 'energia':
            self.hp = 0
            self.score = 100
            self.imagem = Settings.ENERGIA
        elif tipo == 'maca':
            self.hp = 20
            self.score = 20
            self.imagem = Settings.APPLE
        else:
            self.hp = 0
            self.score = 50
            self.imagem = Settings.FOOD

        self.contador = 0
        self.limite_contagem = 2
        self.colider = pygame.Rect(self.x,self.y,Settings.TAMANHO[0],Settings.TAMANHO[1])

    def desenhar(self):
        if self.contador >= 0 and self.contador < self.limite_contagem: imagem = self.imagem[0]
        elif self.contador >= self.limite_contagem and self.contador < 2*self.limite_contagem: imagem = self.imagem[1]
        elif self.contador >= 2*self.limite_contagem and self.contador < 3*self.limite_contagem: imagem = self.imagem[2]
        elif self.contador >= 3*self.limite_contagem and self.contador < 4*self.limite_contagem: imagem = self.imagem[1]
        elif self.contador >= 4*self.limite_contagem:
            imagem = self.imagem[0]
            self.contador = 0

        self.contador += 1
        Settings.TELA.blit(imagem, (self.x, self.y))

class Comida(objetosCapturaveis):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        super().__init__(x,y,'comida')

class Energia(objetosCapturaveis):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        super().__init__(x,y,'energia')

class Apple(objetosCapturaveis):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        super().__init__(x,y,'maca')

class AnimationGame:
    def __init__(self):
        self.contador = 0
        self.limiteContagem = 2
        self.isAniamtionPacManDyingFinished = False

    def animarPacManDying(self,pacMan):
        if self.contador >= 0 and self.contador < self.limiteContagem: pacMan.imagem = Settings.PAC_MAN_MORRENDO[0]
        elif self.contador >= self.limiteContagem and self.contador < 2*self.limiteContagem: pacMan.imagem = Settings.PAC_MAN_MORRENDO[1]
        elif self.contador >= 2*self.limiteContagem and self.contador < 3*self.limiteContagem: pacMan.imagem = Settings.PAC_MAN_MORRENDO[2]
        elif self.contador >= 3*self.limiteContagem and self.contador < 4*self.limiteContagem: pacMan.imagem = Settings.PAC_MAN_MORRENDO[3]
        elif self.contador >= 4*self.limiteContagem and self.contador < 5*self.limiteContagem: pacMan.imagem = Settings.PAC_MAN_MORRENDO[4]
        elif self.contador >= 5*self.limiteContagem and self.contador < 6*self.limiteContagem: pacMan.imagem = Settings.PAC_MAN_MORRENDO[5]
        if self.contador>=6*self.limiteContagem:
            self.contador = 0
            self.isAniamtionPacManDyingFinished = True

        self.contador += 1

    def animarMudancaDeCorDaBarreira(self,corTroca,game):
        isAnimationOver = False
        if self.contador >= 0 and self.contador < self.limiteContagem:
            Settings.COR_BARREIRA = corTroca
        elif self.contador >= self.limiteContagem and self.contador < 2*self.limiteContagem:
            Settings.COR_BARREIRA = Settings.AZUL
        elif self.contador >= 2*self.limiteContagem and self.contador < 3*self.limiteContagem:
            Settings.COR_BARREIRA = corTroca
        elif self.contador >= 4*self.limiteContagem and self.contador < 5*self.limiteContagem:
            Settings.COR_BARREIRA = Settings.AZUL
        elif self.contador >= 5*self.limiteContagem and self.contador < 6*self.limiteContagem:
            Settings.COR_BARREIRA = corTroca
        elif self.contador >= 7*self.limiteContagem:
            self.contador = 0
            Settings.COR_BARREIRA = Settings.AZUL
            isAnimationOver = True

        self.contador += 1
        return isAnimationOver

class Game:
    def __init__(self):
        self.fase = 1
        self.juiz = Juiz()
        self.pacMan = pacMan(-10,-10)
        self.animationGame = AnimationGame()
        self.barreira = Barreiras()
        self.ghosts = []
        self.gerenciadorDeObjetos = gerenciadorDeObjetos()
        self.sensores = []
        self.food = []
        self.energia = []
        self.apple = []
        self.locaisPossiveisParaColocarAsApple = []
        self.contadorParaTrocarAVelocidadeDoGhost = 0
        self.inicioDoJogo = True
        self.inAnimationState = False
        self.isGameOver = False
        self.isNextFase = False
        self.referenciaParaGhostVoltarParaCasa = pygame.Rect(600,30,Settings.TAMANHO[0],Settings.TAMANHO[1])

    def manipularEventos(self,playing,trocarStatusDosGhostsParaAttacker,trocarStatusDosGhostsParaAttacked,criarAppleNoCenario):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                playing = False

            if evento.type == trocarStatusDosGhostsParaAttacker:
                self.trocarStatusDosGhostsParaAttacker()
                pygame.time.set_timer(trocarStatusDosGhostsParaAttacker,0)

            if evento.type == trocarStatusDosGhostsParaAttacked:
                self.trocarStatusDosGhostsParaAttacked()
                pygame.time.set_timer(trocarStatusDosGhostsParaAttacked,0)
                pygame.time.set_timer(trocarStatusDosGhostsParaAttacker,10000)

            if evento.type == criarAppleNoCenario:
                indice = self.criarAppleNoCenario()
                self.deletarPosicoesDasApplesCriadasNaListaDePossiveisPosicoesParaApple(indice)

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RIGHT: self.pacMan.moveRight,self.pacMan.moveLeft,self.pacMan.moveUp,self.pacMan.moveDown = True,False,False,False
                elif evento.key == pygame.K_LEFT: self.pacMan.moveRight,self.pacMan.moveLeft,self.pacMan.moveUp,self.pacMan.moveDown = False,True,False,False
                elif evento.key == pygame.K_UP: self.pacMan.moveRight,self.pacMan.moveLeft,self.pacMan.moveUp,self.pacMan.moveDown = False,False,True,False
                elif evento.key == pygame.K_DOWN: self.pacMan.moveRight,self.pacMan.moveLeft,self.pacMan.moveUp,self.pacMan.moveDown = False,False,False,True

        return playing

    def definirStatsEObjetosNecessariosAoIniciarUmaFase(self,trocarStatusDosGhostsParaAttacker,criarAppleNoCenario):
        Settings.VELOCIDADE_GHOST = 30
        self.contadorParaTrocarAVelocidadeDoGhost = 0
        self.fase = Settings.FASE
        self.criarPacMan()
        self.criarGhostDeAcordoComFase()
        self.pacMan.hp = 100
        self.pacMan.score = Settings.SCORE_ACUMULADO
        self.definirBarreiras()
        self.posicionarSensores()
        posicoesEnergia = self.definirPosicoesDasEnergias()
        self.definirFoodPorTodaTelaDescontandoAsBarreiras(posicoesEnergia)
        self.inserirEnergiaNasSuasPosicoes(posicoesEnergia)
        self.desenharElementosNoCenario()
        self.renderizarATela()
        time.sleep(0.5)
        pygame.time.set_timer(trocarStatusDosGhostsParaAttacker,2000)
        pygame.time.set_timer(criarAppleNoCenario,60000)
        self.inicioDoJogo = False

    def criarPacMan(self): self.pacMan = pacMan(690,390)

    def definirBarreiras(self):
        self.barreira.definirBarreirasCanto()
        self.barreira.definirBarreirasCentrais()
        self.barreira.definirBarreirasFase1() #vamos, a principio, usar o mesmo labirinto para todas as fases... Para facilitar a vida... Hehe

    def posicionarSensores(self):
        #As linhas da lista estão divididas por seção do labirinto. Percorrendo a lista de cima para baixo, da esquerda para a direita, cada linha representa uma seção do labirinto
        #que seguimos na mesma direção (cima para baixo, direita para esquerda)
        self.sensores = [Sensores(30,30,True,False,False,True), Sensores(30,90,True,False,True,False), Sensores(300,30,True,True,False,True), Sensores(300,90,False,True,True,False), Sensores(180,90,True,True,False,True),

                         Sensores(180,150,True,True,True,False), Sensores(30,150,True,False,False,True), Sensores(300,150,False,True,False,True), Sensores(30,210,True,False,True,False), Sensores(180,210,True,True,False,True), Sensores(300,210,True,True,True,False),

                         Sensores(30,270,True,False,False,True), Sensores(180,270,True,True,True,False), Sensores(300,270,True,True,False,True), Sensores(30,330,True,False,True,False), Sensores(180,330,True,True,False,True), Sensores(300,330,False,True,True,False),

                         Sensores(30,390,True,False,False,True), Sensores(180,390,True,True,True,False), Sensores(300,390,True,True,False,True), Sensores(30,450,True,False,True,False), Sensores(300,450,False,True,True,False),

                         Sensores(360,30,True,True,False,True), Sensores(540,30,False,True,False,True), Sensores(360,90,True,False,True,True), Sensores(540,90,True,True,True,False),

                         Sensores(360,150,True,False,True,True), Sensores(540,150,False,True,False,True), Sensores(360,210,True,True,True,True), Sensores(540,210,True,True,True,False),

                         Sensores(360,270,True,True,True,True), Sensores(540,270,False,True,False,True), Sensores(360,330,True,False,True,True), Sensores(540,330,True,True,True,False),

                         Sensores(360,390,True,True,True,True), Sensores(540,390,False,True,False,True), Sensores(360,450,True,False,True,False), Sensores(540,450,True,True,True,False),

                         Sensores(600,30,True,False,False,True), Sensores(780,30,False,True,False,True), Sensores(600,90,True,True,True,True), Sensores(780,90,True,True,True,True), Sensores(600,150,True,False,True,True), Sensores(780,150,False,True,True,True), Sensores(600,210,False,True,True,True), Sensores(780,210,True,False,True,True),

                         Sensores(600,330,True,True,True,True), Sensores(780,330,True,True,True,True), Sensores(600,390,True,False,True,True), Sensores(780,390,False,True,True,True), Sensores(600,450,True,True,True,False), Sensores(780,450,True,True,True,False),

                         Sensores(840,30,True,False,False,True), Sensores(1020,30,True,True,False,True), Sensores(840,90,True,True,True,False), Sensores(1020,90,False,True,True,True),

                         Sensores(840,150,True,False,False,True), Sensores(1020,150,False,True,True,True), Sensores(840,210,True,True,True,False), Sensores(1020,210,True,True,True,True),

                         Sensores(840,270,True,False,False,True), Sensores(1020,270,True,True,True,True), Sensores(840,330,True,True,True,False), Sensores(1020,330, False,True,True,True),

                         Sensores(840,390,True,False,False,True),Sensores(1020,390,True,True,True,True), Sensores(840,450,True,True,True,False), Sensores(1020,450,False,True,True,False),

                         Sensores(1080,30,True,True,False,True), Sensores(1320,30,False,True,False,True), Sensores(1080,90,True,False,True,False), Sensores(1200,90,True,True,False,True), Sensores(1320,90,False,True,True,False),

                         Sensores(1080,150,True,False,False,True), Sensores(1200,150,True,True,True,False), Sensores(1320,150,False,True,False,True), Sensores(1080,210,True,True,True,False), Sensores(1200,210,True,True,False,True), Sensores(1320,210,False,True,True,False),

                         Sensores(1080,270,True,True,False,True), Sensores(1200,270,True,True,True,False), Sensores(1320,270,False,True,False,True), Sensores(1080,330,True,False,True,False), Sensores(1200,330,True,True,False,True), Sensores(1320,330,False,True,True,False),

                         Sensores(1080,390,True,True,False,True), Sensores(1200,390,True,True,True,False), Sensores(1320,390,False,True,False,True), Sensores(1080,450,True,False,True,False), Sensores(1320,450,False,True,True,False),

                         #Aqui, atribuimos os dois sensores qeu ficarão dentro das casas dos ghosts
                         Sensores(660,210,False,True,False,False), Sensores(720,210,True,False,False,False)]

    def definirPosicoesDasEnergias(self):
        return [pygame.Rect(30,30,Settings.TAMANHO[0],Settings.TAMANHO[1]),pygame.Rect(30,450,Settings.TAMANHO[0],Settings.TAMANHO[1]),
                pygame.Rect(Settings.TELA_LARGURA-60,450,Settings.TAMANHO[0],Settings.TAMANHO[1]),pygame.Rect(Settings.TELA_LARGURA-60,30,Settings.TAMANHO[0],Settings.TAMANHO[1]),
                pygame.Rect(360,390,Settings.TAMANHO[0],Settings.TAMANHO[1]),pygame.Rect(840,150,Settings.TAMANHO[0],Settings.TAMANHO[1])]

    def inserirEnergiaNasSuasPosicoes(self,posicoesLivresParaInserirEnergia):
        for i in range(len(posicoesLivresParaInserirEnergia)):
            self.energia.append(Energia(posicoesLivresParaInserirEnergia[i].x,posicoesLivresParaInserirEnergia[i].y))

    def definirFoodPorTodaTelaDescontandoAsBarreiras(self,posicoesLivresParaInserirEnergia = []):
        posicaoCentralOndeNaoHaveraComida = [pygame.Rect(660,210,Settings.TAMANHO[0],Settings.TAMANHO[1]),pygame.Rect(690,210,Settings.TAMANHO[0],Settings.TAMANHO[1]),pygame.Rect(720,210,Settings.TAMANHO[0],Settings.TAMANHO[1]),
                                             pygame.Rect(660,240,Settings.TAMANHO[0],Settings.TAMANHO[1]),pygame.Rect(690,240,Settings.TAMANHO[0],Settings.TAMANHO[1]),pygame.Rect(720,240,Settings.TAMANHO[0],Settings.TAMANHO[1]),
                                             pygame.Rect(660,270,Settings.TAMANHO[0],Settings.TAMANHO[1]),pygame.Rect(690,270,Settings.TAMANHO[0],Settings.TAMANHO[1]),pygame.Rect(720,270,Settings.TAMANHO[0],Settings.TAMANHO[1]),]

        for linha in range(0,Settings.TELA_ALTURA,Settings.TAMANHO[1]):
            for coluna in range(0,Settings.TELA_LARGURA,Settings.TAMANHO[0]):
                objetoFood = Comida(coluna,linha)
                if objetoFood.colider not in self.barreira.barreiras and objetoFood.colider not in posicaoCentralOndeNaoHaveraComida and objetoFood.colider not in posicoesLivresParaInserirEnergia:
                    self.food.append(objetoFood)

    def criarAppleNoCenario(self):
        if len(self.locaisPossiveisParaColocarAsApple) > 0:
            indice = random.randrange(len(self.locaisPossiveisParaColocarAsApple))
            self.apple.append(Apple(self.locaisPossiveisParaColocarAsApple[indice][0],self.locaisPossiveisParaColocarAsApple[indice][1]))
            return indice

    def deletarPosicoesDasApplesCriadasNaListaDePossiveisPosicoesParaApple(self,indice):
        self.gerenciadorDeObjetos.deletarObjetoDaLista(self.locaisPossiveisParaColocarAsApple,self.locaisPossiveisParaColocarAsApple[indice])

    def criarGhostDeAcordoComFase(self):
        if self.fase == 1: self.ghosts = [Ghost(660,210,Settings.GHOST_AMARELO)]
        if self.fase == 2: self.ghosts = [Ghost(660,210,Settings.GHOST_AMARELO),Ghost(720,210,Settings.GHOST_VERMELHO)]
        if self.fase == 3: self.ghosts = [Ghost(660,210,Settings.GHOST_AMARELO),Ghost(660,210,Settings.GHOST_AMARELO),Ghost(720,210,Settings.GHOST_VERMELHO)]
        if self.fase == 4: self.ghosts = [Ghost(660,210,Settings.GHOST_AMARELO),Ghost(660,210,Settings.GHOST_AMARELO),Ghost(720,210,Settings.GHOST_VERMELHO),Ghost(720,210,Settings.GHOST_VERMELHO)]
        if self.fase == 5: self.ghosts = [Ghost(660,210,Settings.GHOST_AMARELO),Ghost(660,210,Settings.GHOST_AMARELO),Ghost(660,210,Settings.GHOST_AMARELO),Ghost(720,210,Settings.GHOST_VERMELHO),Ghost(720,210,Settings.GHOST_VERMELHO),Ghost(720,210,Settings.GHOST_VERMELHO)]

    def trocarStatusDosGhostsParaAttacker(self):
        for each_ghost in self.ghosts:
            if not each_ghost.state == 'Recovering': each_ghost.state = each_ghost.states[1]

    def trocarStatusDosGhostsParaAttacked(self):
        for each_ghost in self.ghosts:
            if not each_ghost.state == 'Recovering': each_ghost.state = each_ghost.states[2]

    def apresentarTextosNaTela(self):
        score = Settings.FONTE_SCORE.render(f"SCORE: {self.pacMan.score}", 1, Settings.BRANCA)
        hp = Settings.FONTE_SCORE.render(f"HP: {self.pacMan.hp}", 1, Settings.BRANCA)

        Settings.TELA.blit(score, (20, 0))
        Settings.TELA.blit(hp, (300, 0))

        if self.inicioDoJogo and not self.inAnimationState:
            ready = Settings.FONTE_READY.render("READY?", 1, Settings.VERMELHA)
            Settings.TELA.blit(ready, (Settings.TELA_LARGURA/2 - ready.get_width()/2, Settings.TELA_ALTURA/2 - ready.get_height()/2))

        if Settings.FASE > 5:
            final_score = Settings.FONTE_SCORE.render(f"YOUR TOTAL SCORE: {Settings.SCORE_ACUMULADO}", 1, Settings.BRANCA)
            Settings.TELA.blit(final_score, (Settings.TELA_LARGURA/2 - final_score.get_width()/2, Settings.TELA_ALTURA/2 - final_score.get_height()/2))

    def desenharHpDoPacManEmBarra(self):
        x = 400
        widthBar = 2
        cor = Settings.VERDE_ESCURO
        if self.pacMan.hp > 40 and self.pacMan.hp<=60: cor = Settings.AMARELO
        elif self.pacMan.hp <= 40: cor = Settings.VERMELHA

        for i in range(1,self.pacMan.hp+1,1):
            pygame.draw.rect(Settings.TELA,cor,[x,10,widthBar,15])
            x += widthBar

    def desenharElementosNoCenario(self):
        #for each_sensor in self.sensores:
            #each_sensor.desenhar()

        #pygame.draw.rect(Settings.TELA,Settings.AMARELO,[self.referenciaParaGhostVoltarParaCasa.x,self.referenciaParaGhostVoltarParaCasa.y,30,30])
        if len(self.food) > 0:
            for each_food in self.food: each_food.desenhar()
        if len(self.energia) > 0:
            for each_energia in self.energia: each_energia.desenhar()
        if len(self.apple) > 0:
            for each_apple in self.apple: each_apple.desenhar()
        for each_ghost in self.ghosts: each_ghost.desenhar()
        self.pacMan.desenhar(self)

        self.barreira.desenhar()

        self.apresentarTextosNaTela()
        self.desenharHpDoPacManEmBarra()

    def atualizarPosicaoDosColiders(self):
        self.pacMan.colider.x, self.pacMan.colider.y = self.pacMan.x, self.pacMan.y
        for each_ghost in self.ghosts: each_ghost.colider.x,each_ghost.colider.y = each_ghost.x, each_ghost.y

    def moverReferenciaParaOghostEncontrarSuaCasa(self):
        if self.referenciaParaGhostVoltarParaCasa.y == 30:
            if self.referenciaParaGhostVoltarParaCasa.x < 780: self.referenciaParaGhostVoltarParaCasa.x += 10

        if self.referenciaParaGhostVoltarParaCasa.x == 780:
            if self.referenciaParaGhostVoltarParaCasa.y < 450: self.referenciaParaGhostVoltarParaCasa.y += 10

        if self.referenciaParaGhostVoltarParaCasa.y == 450:
            if self.referenciaParaGhostVoltarParaCasa.x > 600: self.referenciaParaGhostVoltarParaCasa.x -= 10

        if self.referenciaParaGhostVoltarParaCasa.x == 600:
            if self.referenciaParaGhostVoltarParaCasa.y > 30: self.referenciaParaGhostVoltarParaCasa.y -= 10

    def deletarObjetosCapturadosPeloPacManDeSuasRespctivasListas(self,objetosCapturados):
        for each_objeto in objetosCapturados:
            if type(each_objeto) is Comida: self.food = self.gerenciadorDeObjetos.deletarObjetoDaLista(self.food,each_objeto)
            if type(each_objeto) is Energia: self.energia = self.gerenciadorDeObjetos.deletarObjetoDaLista(self.energia,each_objeto)
            if type(each_objeto) is Apple: self.apple = self.gerenciadorDeObjetos.deletarObjetoDaLista(self.apple,each_objeto)

    def alterarStatusDeGhostsCasoPacManTenhaCapturadoUmaEnergia(self,trocarStatusDosGhostsParaAttacked,objetosCapturados):
        energia = list(filter(lambda objeto: type(objeto) == Energia,objetosCapturados))
        if len(energia) > 0: pygame.time.set_timer(trocarStatusDosGhostsParaAttacked,1)

    def atribuirScoreAoPacManPorCadaGhostNoEstadoRecovering(self):
        for each_ghost in self.ghosts:
            if each_ghost.state == 'Recovering' and not each_ghost.pacManJaGanhouScoreSobreMim:
                self.pacMan.score += each_ghost.scoreParaOPAcMan
                each_ghost.pacManJaGanhouScoreSobreMim = True #voltará a ser False quando o ghost atingir o status de Attacker novamente

    def apresentarNaTelaOScoreAtribuidoACadaGhost(self):
        for each_ghost in self.ghosts:
            if each_ghost.state == 'Recovering':
                if each_ghost.contadorDeTempoDaMensagemDePontuacaoQuandoOPacManComeOGhost <= 10:
                    texto = Settings.FONTE.render(f"+{each_ghost.scoreParaOPAcMan}", 1, Settings.BRANCA)
                    Settings.TELA.blit(texto, (each_ghost.x, each_ghost.y+20))
                each_ghost.contadorDeTempoDaMensagemDePontuacaoQuandoOPacManComeOGhost += 1

    def recuperarPossiveisPosicoesParaImplementarApple(self,objetosCapturados):
        self.locaisPossiveisParaColocarAsApple += list(map(lambda objeto: (objeto.x,objeto.y),objetosCapturados))

    def controlarPacMan(self,trocarStatusDosGhostsParaAttacked):
        objetosNoCenario = self.food + self.energia + self.apple
        self.pacMan.mover(self.barreira.barreiras,Settings.VELOCIDADE_PACMAN)
        objetosCapturados = self.pacMan.verificarSeObjetosForamCapturados(objetosNoCenario)
        if len(objetosCapturados) > 0:
            self.pacMan.alterarOsAtributosAposACapturaDeObjetosNoCenario(objetosCapturados)
            self.alterarStatusDeGhostsCasoPacManTenhaCapturadoUmaEnergia(trocarStatusDosGhostsParaAttacked,objetosCapturados)
            self.recuperarPossiveisPosicoesParaImplementarApple(objetosCapturados)
            self.deletarObjetosCapturadosPeloPacManDeSuasRespctivasListas(objetosCapturados)

        #caso algum ghost tenha sido pego no seu modo attacked...
        self.atribuirScoreAoPacManPorCadaGhostNoEstadoRecovering()
        self.apresentarNaTelaOScoreAtribuidoACadaGhost()

    def zerarStatsAoMudarDeFase(self):
        self.pacMan.moveRight,self.pacMan.moveLeft,self.pacMan.moveUp,self.pacMan.moveDown = False,False,False,False
        self.pacMan.lookingRight,self.pacMan.lookingLeft,self.pacMan.lookingUp,self.pacMan.lookingDown = True,False,False,False
        self.locaisPossiveisParaColocarAsApple.clear()
        self.inicioDoJogo = True

    def zerarStatsAposFimDeAnimacao(self):
        self.apple.clear()
        self.food.clear()
        self.energia.clear()
        self.sensores.clear()
        self.barreira.barreiras.clear()
        self.ghosts.clear()
        self.isNextFase = False
        self.isGameOver = False
        self.inAnimationState = False
        self.animationGame.isAniamtionPacManDyingFinished = False

    def controlarMudancaDeFase(self,contadorDeEntradaNoJogo):
        mudouDeFase = self.juiz.verificarMudancaDeFase(self.food)
        if mudouDeFase:
            self.zerarStatsAoMudarDeFase()
            Settings.SCORE_ACUMULADO = self.pacMan.score
            contadorDeEntradaNoJogo = 0
            self.inAnimationState = True
            self.isNextFase = True
            Settings.FASE += 1

        return contadorDeEntradaNoJogo

    def verificarGameOver(self,contadorDeEntradaNoJogo):
        isGameOver = self.juiz.verificarGameOver(self.pacMan)
        if isGameOver:
            self.zerarStatsAoMudarDeFase()
            Settings.SCORE_ACUMULADO = 0
            contadorDeEntradaNoJogo = 0
            self.inAnimationState = True
            self.isGameOver = True
            self.pacMan.score = 0
            Settings.FASE = 1

        return contadorDeEntradaNoJogo

    def renderizarAnimacaoDeFimDeCiclos(self):
        if self.isNextFase:
            isAnimationOver = self.animationGame.animarMudancaDeCorDaBarreira(Settings.AMARELO,self)
        elif self.isGameOver:
            isAnimationOver = False
            if not self.animationGame.isAniamtionPacManDyingFinished:self.animationGame.animarPacManDying(self.pacMan)
            else:isAnimationOver = self.animationGame.animarMudancaDeCorDaBarreira(Settings.VERMELHA,self)

        return isAnimationOver

    def moverGhosts(self):
        for each_ghost in self.ghosts:
            #aqui atribuimos a velocidade dessa forma, para que todos os ghosts possam sofrer a variação de velocidade ditada no método trocarAVelocidadeDoGhost
            each_ghost.velocidade = Settings.VELOCIDADE_GHOST
            #este método move o rect que servirá como referência para os ghosts seguirem quando eles estiverem em estado de Recover
            #basicamente, temos um retangulo que fica dando voltas no centro do cenário e servirá de auxilio como um ponto de referencia móvel para os ghosts
            self.moverReferenciaParaOghostEncontrarSuaCasa()

            possiveisDirecoes = each_ghost.definirPossiveisDirecoesAPartirDeUmPontoDeSensor(self.sensores)
            if len(possiveisDirecoes) > 0:
                #O estágio breeding atua logo no início do jogo, onde por 5 segundos os ghosts se afastam do pacMan.
                if each_ghost.state == 'Breeding' or each_ghost.state == 'Atacked': #neste caso, os ghosts se afastam do pacMan
                    listaDeDistanciasDoPontoDereferencia = each_ghost.definirDistanciasDoPontoDeReferencia(possiveisDirecoes,self.pacMan.colider)
                    each_ghost.definirMelhorDirecaoParaSeAfastarDoPacMan(listaDeDistanciasDoPontoDereferencia,self.gerenciadorDeObjetos)

                #no estágio Attacker, os ghosts perseguirão o pacMan
                elif each_ghost.state == 'Attacker': #neste caso, os ghosts buscam o pacMan
                    listaDeDistanciasDoPontoDereferencia = each_ghost.definirDistanciasDoPontoDeReferencia(possiveisDirecoes,self.pacMan.colider)
                    each_ghost.definirMelhorDirecaoParaseguirPacMan(listaDeDistanciasDoPontoDereferencia,self.gerenciadorDeObjetos)

                # O estágio Recovering acontece quando o pacMan captura os ghosts, depois disso eles vão procurar a casa de recuperação de status.
                elif each_ghost.state == 'Recovering': #neste caso, os ghosts buscam sua casa
                    listaDeDistanciasDoPontoDereferencia = each_ghost.definirDistanciasDoPontoDeReferencia(possiveisDirecoes,self.referenciaParaGhostVoltarParaCasa)
                    each_ghost.definirDirecaoParaVoltarParaCasa(listaDeDistanciasDoPontoDereferencia,self.gerenciadorDeObjetos)
                    #método que transforma o estado do ghost para Attacker quando ele voltar para sua casa
                    each_ghost.voltarASerAtackerDepoisDoRecover()

            #verificamos as possiveis colisões com o pacMan aqui, fora do bloco if len(possiveisDirecoes) > 0.
            #se dentro do bloco, a verificação só seria feita nos momentos em que o ghost passasse pelos sensores
            if each_ghost.state == 'Atacked': each_ghost.colideWithPacManAsAnAttacked(self.pacMan)
            if each_ghost.state == 'Attacker': each_ghost.colideWithPacManAsAnAttacker(self.pacMan)

            each_ghost.mover(self.barreira.barreiras,each_ghost.velocidade)
            if each_ghost.velocidade == 30: each_ghost.seSepararDeGhostsQueCruzamNoMesmoPonto(self.ghosts,self.barreira.barreiras)

    def renderizarATela(self): pygame.display.update()

    def trocarAVelocidadeDoGhost(self):
        self.contadorParaTrocarAVelocidadeDoGhost += 1
        if Settings.VELOCIDADE_GHOST == 30:
            if self.contadorParaTrocarAVelocidadeDoGhost == 20:
                Settings.VELOCIDADE_GHOST = 15
                self.contadorParaTrocarAVelocidadeDoGhost = 0
        else:
            if self.contadorParaTrocarAVelocidadeDoGhost == 4:
                Settings.VELOCIDADE_GHOST = 30
                self.contadorParaTrocarAVelocidadeDoGhost = 0

class Juiz:
    def verificarMudancaDeFase(self,listaFood):
        if len(listaFood) == 0:
            return True
        return False

    def verificarGameOver(self,pacMan):
        if pacMan.hp <= 0:
            return True
        return False

class gerenciadorDeObjetos:

    def ordenarListaDeTuplasEmOrdemCrescente(self,lista):
        for i in range(len(lista)):
            for j in range(len(lista)):
                if lista[i][0] < lista[j][0]:
                    tupla = lista[i]
                    lista[i] = lista[j]
                    lista[j] = tupla
        return lista

    def ordenarListaDeTuplasEmOrdemDecrescente(self,lista):
        for i in range(len(lista)):
            for j in range(len(lista)):
                if lista[i][0] > lista[j][0]:
                    tupla = lista[i]
                    lista[i] = lista[j]
                    lista[j] = tupla
        return lista

    def deletarObjetoDaLista(self,listaDeObjetos,objeto):
        return list(filter(lambda obj: obj != objeto,listaDeObjetos))
