
import pygame

from classesGame import *

def main():
    playing = True
    game = Game()
    contadorDeEntradaNoJogo = 0

    trocarStatusDosGhostsParaAttacker = pygame.USEREVENT + 1
    trocarStatusDosGhostsParaAttacked = pygame.USEREVENT + 2
    criarAppleNoCenario = pygame.USEREVENT + 3


    while playing:
        Settings.RELOGIO.tick(Settings.VELOCIDADE_JOGO)
        Settings.TELA.fill(Settings.PRETA)
        playing = game.manipularEventos(playing,trocarStatusDosGhostsParaAttacker,trocarStatusDosGhostsParaAttacked,criarAppleNoCenario)
        if not game.inAnimationState:
            #queremos atribuir os elementos no cenário apenas uma vez, por isso usamos do recurso do contador
            #poderiamos instanciar isso fora do loop, porém, aqui fica mais fácil para implementar a mudança de fase
            if contadorDeEntradaNoJogo == 0:
                game.definirStatsEObjetosNecessariosAoIniciarUmaFase(trocarStatusDosGhostsParaAttacker,criarAppleNoCenario)
                contadorDeEntradaNoJogo += 1

            game.desenharElementosNoCenario()

            game.controlarPacMan(trocarStatusDosGhostsParaAttacked)
            game.moverGhosts()

            game.atualizarPosicaoDosColiders()
            game.renderizarATela()
            game.trocarAVelocidadeDoGhost()

            contadorDeEntradaNoJogo = game.controlarMudancaDeFase(contadorDeEntradaNoJogo)
            contadorDeEntradaNoJogo = game.verificarGameOver(contadorDeEntradaNoJogo)
        else:
            isAnimationOver = game.renderizarAnimacaoDeFimDeCiclos()
            game.desenharElementosNoCenario()
            game.renderizarATela()
            if isAnimationOver: game.zerarStatsAposFimDeAnimacao()

            #Finalizando o jogo
            if Settings.FASE > 5:
                time.sleep(10)
                playing = False


if __name__ == '__main__':
    main()



