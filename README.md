Um motor, servidor, cliente e visualizador para jogar Boku feito em Python 3.

Nota: o Jupyter Notebook está deprecado.

## Requerimentos
* Python 3

## Executando

```
./python server.py
```

Use um navegador para acessar o endereço `http://localhost:8080/visualizador.html`.

## Cliente

Um cliente que faz jogadas aleatórias está disponível (`random_client.py`). Para utilizá-lo, rode o servidor e execute o cliente passando como parâmetro o número do jogador (1 ou 2). Pode-se rodar dois clientes simultâneamente, cada um com um número de jogador. 

## API

A API ainda está em desenvolvimento. Estão disponíveis funcionalidades básicas, que são acessadas por http.

* `/jogador`. Retorna o número do jogador de quem é a vez de jogar. Retorna 0 se o jogo acabou e o oponente venceu.
* `/tabuleiro`. Retorna o estado atual do tabuleiro, na forma de lista de listas. Cada lista representa uma coluna. O valor `0` representa um espaço vazio, enquanto `1` representa o primeiro jogador e `2` representa os segundo jogador.
* `/move?player=X&coluna=C&linha=L`. Coloca uma peça do jogador X na coluna C e linha L. Retorna uma tupla `(erro, msg)`. Se `erro<0`, `msg` conterá o erro ocorrido. Se `erro==0`, o movimento feito encerrou o jogo e o cliente venceu. 
* `/reiniciar`. Reinicia o jogo, limpando o tabuleiro.
* `/ultima_jogada`. Retorna a posição da última jogada realizada (coluna, linha).
* `/movimentos`. Retorna uma lista de posições válidas (coluna,linha) onde o jogador atual pode colocar uma peça (ou remover uma peça do adversário).
* `/num_movimentos`. Retorna o número de movimentos realizados desde o início do jogo.
