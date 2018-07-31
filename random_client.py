import urllib.request
import sys
import random
import time

if len(sys.argv)==1:
    print("Voce deve especificar o numero do jogador (1 ou 2)\n\nExemplo:    ./random_client.py 1")
    quit()

# Alterar se utilizar outro host
host = "http://localhost:8080"

player = int(sys.argv[1])

# Reinicia o tabuleiro
resp = urllib.request.urlopen("%s/reiniciar" % host)

done = False
while not done:
    # Pergunta quem eh o jogador
    resp = urllib.request.urlopen("%s/jogador" % host)
    player_turn = int(resp.read())

    # Se jogador == 0, o jogo acabou e o cliente perdeu
    if player_turn==0:
        print("I lose.")
        done = True

    # Se for a vez do jogador
    if player_turn==player:
        # Pega os movimentos possiveis
        resp = urllib.request.urlopen("%s/movimentos" % host)
        movimentos = eval(resp.read())

        # Escolhe um movimento aleatoriamente
        movimento = random.choice(movimentos)

        # Executa o movimento
        resp = urllib.request.urlopen("%s/move?player=%d&coluna=%d&linha=%d" % (host,player,movimento[0],movimento[1]))
        msg = eval(resp.read())

        # Se com o movimento o jogo acabou, o cliente venceu
        if msg[0]==0:
            print("I win")
            done = True
        if msg[0]<0:
            raise Exception(msg[1])
    
    # Descansa um pouco para nao inundar o servidor com requisicoes
    time.sleep(1)




