Alunos: Alesom Zorzi, Igor Beilner e Régis Thiago Feyh
Disciplina: Computação Distribuida

DISTRIBUTED TETRIS

O objetivo é fazer um jogo de tetris distribuido. 
Todas as pessoas conectadas no jogo farão sua jogada e a cada jogada feita o sistema computada a jogada de todos os jogadores, a jogada mais votada se torna real. 


No servidor ficará a o estado global do jogo, quando o jogador (cliente) terminar sua jogada será enviado ao servidor a posição de onde foi colocada a peça. 
O servidor assim recebe todos os votos e depois de computados os votos o servidor envia ao cliente a resposta da votação atualizando assim o tabuleiro do usuário caso a escolha votada tenha sido diferente da jogador.


