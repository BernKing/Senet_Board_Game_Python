#Turma pratica 4~
#Implementação do Senet realizado por:
#Bernardo Almeida, al78403
#Vasco Macedo, al78798

import random
import os

tabuleiro =      [["__"] * 10 for _ in range(3)]

preta_pieces =   {"P1": (0, 0), "P2": (0, 2), "P3": (0, 4), "P4": (0, 6), "P5": (0, 8)}
branca_pieces =  {"B1": (0, 1), "B2": (0, 3), "B3": (0, 5), "B4": (0, 7), "B5": (0, 9)}

preta_nova =     {"P1": (0, 0), "P2": (0, 0), "P3": (0, 0), "P4": (0, 0), "P5": (0, 0)}
branca_nova =    {"B1": (0, 0), "B2": (0, 0), "B3": (0, 0), "B4": (0, 0), "B5": (0, 0)}

preta_retirar =  {"P1": (0, 0), "P2": (0, 0), "P3": (0, 0), "P4": (0, 0), "P5": (0, 0)}
branca_retirar = {"B1": (0, 0), "B2": (0, 0), "B3": (0, 0), "B4": (0, 0), "B5": (0, 0)}

#Branca Preta
nomes = ["", ""]

def retirar_peca(posicao,dado):
    if posicao == (2,7) and dado == 3:
        return 0
    elif posicao == (2,8) and dado == 2:
        return 0
    elif posicao == (2,9) and dado == 1:
        return 0
    else:
        return 1

#Algoritmo para ver a posicao futura da peça com base no dado
def andar_casas(posicao, dado):
    linha, col = posicao
    if linha == 0:
        col += dado
        if col > 9:
            linha = 1
            col = 9 - (col % 10)
    elif linha == 1:
        col -= dado
        if col < 0:
            linha = 2
            col = abs(col) - 1
    elif linha == 2:
        var = col
        col += dado
        if col > 9:
            linha = 2
            col = var
    posicao = linha, col
    return posicao

def andar_casas_reverse(posicao,dado):
    linha, col = posicao
    if linha == 0:
        var = col
        col -= dado
        if col < 0:
            linha = 0
            col = var
    elif linha == 1:
        col += dado
        if col > 9:
            linha = 0
            col = 9 - (col % 10)
    elif linha == 2:
        var = col
        col -= dado
        if col < 0:
            linha = 1
            col = abs(col) - 1
    posicao = linha, col
    return posicao

def testar_condicoes(dado, jogador, peca_imovel):
    pieces = preta_pieces if jogador == "preta" else branca_pieces
    nova_pieces = preta_nova if jogador == "preta" else branca_nova
    peca_retirar = preta_retirar if jogador == "preta" else branca_retirar

    for chave, posicao in pieces.items():
        linha, col = posicao

        if linha == 0:
            col += dado
            if col > 9:
                linha = 1
                col = 9 - (col % 10)
        elif linha == 1:
            col -= dado
            if col < 0:
                linha = 2
                col = abs(col) - 1
        elif linha == 2:
            var = col
            col += dado
            if col > 5:

                linha = 2
                col = var

        posicao_atualizada = linha, col

        cont = 0

        if posicao == (2,5):
            if dado == 5:
                peca_retirar[chave] = (9,9)
                #print(f"{chave}: Pode retirar esta peça.")
                print('\033[31m' + f"{chave}: Pode retirar esta peça." + '\033[0m')
                continue

            elif dado <= 4:
                posicao_atualizada = andar_casas(posicao, dado)
                linha, col = posicao_atualizada
            


        for coordenada in pieces.values():
            if coordenada == posicao_atualizada and posicao_atualizada != (2,6) and posicao_atualizada != (2,7) and posicao_atualizada != (2,8) and posicao_atualizada != (2,9):
                cont += 1
        if cont == 0:  

            if retirar_peca(posicao,dado) == 0:
                peca_retirar[chave] = (9,9)
                #print(f"{chave}: Pode retirar esta peça.")
                print('\033[31m' + f"{chave}: Pode retirar esta peça." + '\033[0m')

            elif tabuleiro[linha][col] != "__":
                #adicionar condição para casa da vida e casa especial antes da saida do tabuleiro
                if linha == 2 and col == 5 or linha == 1 and col == 5 or linha == 2 and col == 6 or linha == 2 and col == 7 or linha == 2 and col == 8 or linha == 2 and col == 9:
                        print(f"{chave}: Não se pode mover esta peça")
                        peca_imovel += 1
                else:
                    if dois_condicao(posicao_atualizada, jogador) == 0 and tres_condicao(posicao, dado, jogador) == 0:
                        nova_pieces[chave] = posicao_atualizada
                        print('\033[32m' + f"{chave}: Se você jogar vai para esta posição: {posicao_atualizada}" + '\033[0m')
                        #f"{chave}: Se você jogar vai para esta posição: {posicao_atualizada}"
                    else:
                        print(f"{chave}: Não se pode mover esta peça")
                        peca_imovel += 1

            elif tabuleiro[linha][col] == "__" :
                
                if tres_condicao(posicao,dado, jogador) == 0:
                    nova_pieces[chave] = posicao_atualizada
                    print('\033[32m' + f"{chave}: Se você jogar vai para esta posição: {posicao_atualizada}" + '\033[0m')
                else:
                    print(f"{chave}: Não se pode mover esta peça")
                    peca_imovel += 1


            else:
                nova_pieces[chave] = posicao_atualizada
                print('\033[32m' + f"{chave}: Se você jogar vai para esta posição: {posicao_atualizada}" + '\033[0m')

        else:
            print(f"{chave}: Não se pode mover esta peça")
            peca_imovel += 1

    return peca_imovel

#Condição das barreiras de 3 peças
def tres_condicao(posicao, andar, jogador):
    pretas = ["P1", "P2", "P3", "P4", "P5"]
    brancas = ["B1", "B2", "B3", "B4", "B5"]
    map_brancas = []
    map_pretas = []

    if jogador == "preta":
        for i in range(andar): #i retirado
            nova_linha, nova_coluna = andar_casas(posicao, 1)
            if tabuleiro[nova_linha][nova_coluna] in brancas:
                posicao = nova_linha, nova_coluna
                map_brancas.append(posicao)
            posicao = nova_linha, nova_coluna
        if len(map_brancas) >= 3:
            if andar_casas(map_brancas[0], 2) == andar_casas(map_brancas[1], 1) == map_brancas[2]:
                return 1
            else:
                return 0

        else:
            return 0
    else:
        for i in range(andar):
            nova_linha, nova_coluna = andar_casas(posicao, 1)
            if tabuleiro[nova_linha][nova_coluna] in pretas:
                posicao = nova_linha, nova_coluna
                map_pretas.append(posicao)
            posicao = nova_linha, nova_coluna
        if len(map_pretas) >= 3:
            if andar_casas(map_pretas[0], 2) == andar_casas(map_pretas[1], 1) == map_pretas[2]:
                return 1
            else:
                return 0
        else:
            return 0

#Condição dos pares
def dois_condicao(posicao_atualizada, jogador):
    pieces = preta_pieces if jogador == "branca" else branca_pieces

    contador = 0
    if jogador == "preta":
        if andar_casas(posicao_atualizada, 1) in pieces.values() or andar_casas_reverse(posicao_atualizada, 1) in pieces.values():
            contador += 1
    else:
        if andar_casas(posicao_atualizada, 1) in pieces.values() or andar_casas_reverse(posicao_atualizada, 1) in pieces.values():
            contador += 1

    return contador


# Ver se peça pertence ao jogador e se é peça valida com base nos resultados da testar condições
def is_jogador_atual_piece(piece, jogador_atual):
    if jogador_atual == "preta" and piece in preta_pieces:
        if preta_nova[piece] != (0,0):
            return True
        else:
            False
    elif jogador_atual == "branca" and piece in branca_pieces:
        if branca_nova[piece] != (0,0):
            return True
        else:
            False
    else:
        False

# Função que corre se o movimento a fazer for para uma casa já ocupada
def posicao_ocupada(piece_to_move, new_linha, new_col, jogador_atual):
    occupying_piece = tabuleiro[new_linha][new_col]

    linha, col = preta_pieces[piece_to_move] if jogador_atual == "preta" else branca_pieces[piece_to_move]
    tabuleiro[new_linha][new_col] = piece_to_move
    tabuleiro[linha][col] = occupying_piece
    if jogador_atual == "preta":
        preta_pieces[piece_to_move] = (new_linha, new_col)
        branca_pieces[occupying_piece] = (linha, col)
    else:
        branca_pieces[piece_to_move] = (new_linha, new_col)
        preta_pieces[occupying_piece] = (linha, col)
        print("Peça Movida!")

#Função que trata da movimentação das peças
def movimento_linha_coluna(piece_to_move, jogador_atual):
    retirar = [(2,5),(2,7),(2,8),(2,9)]
    remover = preta_retirar if jogador_atual == "preta" else branca_retirar

    if jogador_atual == "preta":
        new_linha = preta_nova[piece_to_move][0]
        new_col = preta_nova[piece_to_move][1]
    else:
        new_linha = branca_nova[piece_to_move][0]
        new_col = branca_nova[piece_to_move][1]

    position = preta_pieces.get(piece_to_move) or branca_pieces.get(piece_to_move)
    linha, col = position
    

    if position in retirar and remover[piece_to_move] == (9,9):
        tabuleiro[linha][col] = "__"
        if jogador_atual == "preta":
            del preta_nova[piece_to_move]
            del preta_pieces[piece_to_move]
        else:
            del branca_nova[piece_to_move]
            del branca_pieces[piece_to_move]

        print("Peça Removida!")

    elif tabuleiro[new_linha][new_col] == "__":
        if new_linha == 2 and new_col == 6:
            tabuleiro[linha][col] = "__"
            
            nova_pos = casa_agua()

            new_linha, new_col = nova_pos[0], nova_pos[1]

            tabuleiro[new_linha][new_col] = piece_to_move
            if jogador_atual == "preta":
                preta_pieces[piece_to_move] = (new_linha, new_col)
                print("Peça Movida!\n")
            else:
                branca_pieces[piece_to_move] = (new_linha, new_col)
                print("Peça Movida!\n")

        else:
            tabuleiro[linha][col] = "__"
            tabuleiro[new_linha][new_col] = piece_to_move
            if jogador_atual == "preta":
                preta_pieces[piece_to_move] = (new_linha, new_col)
                print("Peça Movida!\n")
            else:
                branca_pieces[piece_to_move] = (new_linha, new_col)
                print("Peça Movida!\n")

    else:
        posicao_ocupada(piece_to_move, new_linha, new_col, jogador_atual)
        
# print tabuleiro
def print_tabuleiro():
    # meter pretas no tabuleiro
    for piece, position in preta_pieces.items():
        linha, col = position
        tabuleiro[linha][col] = piece

    # meter peças brancas no tabuleiro
    for piece, position in branca_pieces.items():
        linha, col = position
        tabuleiro[linha][col] = piece

    for linha_index, linha in enumerate(tabuleiro):
        for col_index, elemento in enumerate(linha):
            if (linha_index, col_index) == (1, 5):
                print("\033[33m" + elemento + "\033[0m", end="  ")  #  (1, 5)  amarelo
            elif linha_index == 2 and 5 <= col_index <= 9:
                if col_index == 5:
                   print("\033[33m" + elemento + "\033[0m", end="  ")  # (2, 5)  amarelo
                elif col_index == 6:
                    print("\033[34m" + elemento + "\033[0m", end="  ")  #  (2, 6)  azul
                else:
                    print("\033[31m" + elemento + "\033[0m", end="  ")  #  (2,7) (2, 8)  (2, 9)  laranja
            else:
                element_spacing = " " if len(elemento) == 1 else ""  # ajustar ewspaço baseado na linha
                print(elemento + element_spacing, end="  ")  # esapaço duplo
        print()  # Newline

    print("\n")

def casa_agua():
    for i in range(9):
        if tabuleiro[0][i] == "__":
            return (0,i)
    
def bot(posicao,jogador_atual):
    pieces = preta_pieces if jogador_atual == "preta" else branca_pieces
    pontos = 0
    #estratégia como defensivo
    condicoes = {
        (2, 6): -10,
        andar_casas(posicao, 1) in pieces.values() or andar_casas_reverse(posicao, 1) in pieces.values(): 5,
        andar_casas(posicao, 1) in pieces.values() and andar_casas_reverse(posicao, 1) in pieces.values(): 1,
        (1, 5): 3,
        posicao in branca_pieces.values(): 2,
        (2, 5): 6,
        posicao in [(2, 7), (2, 8), (2, 9)]: 4
    }
    
    for condition, points in condicoes.items():
        if condition:
            pontos += points

    return pontos

#Modo de jogo 2, input do user e parte do algoritmo do bot
def peca_mover_dois():
    piece_to_move = input("Peça que queres mover (ou q para sair): ")
    if piece_to_move.lower() == "q":
        exit()
    else:
        piece_to_move = piece_to_move[0].upper() + piece_to_move[1:]

    return piece_to_move
#modo de jogo 1, input do user
def peca_mover(jogador_atual):
    #HUMANO
    if jogador_atual == "branca":
        piece_to_move = input("Peça que queres mover (ou q para sair): ")
    
        if piece_to_move.lower() == "q":
            os.system('cls' if os.name == 'nt' else 'clear')
            exit()
        elif piece_to_move:
            piece_to_move = piece_to_move[0].upper() + piece_to_move[1:]

        return piece_to_move
    
    #BOT
    else:
        print("Peça que queres mover: ")
        nova_pieces = preta_nova if jogador_atual == "preta" else branca_nova#AQUIII
        peca_retirar = preta_retirar if jogador_atual == "preta" else branca_retirar
        
        maximo = []

        pontos = []
        chaves_filtradas_nova = [key for key, value in nova_pieces.items() if value != (0, 0)]
        for chave in chaves_filtradas_nova:
            ponto = bot(nova_pieces[chave], jogador_atual)

            pontos.append(ponto)
        #variavel inicia com menor float possivel
        max_number = float('-inf')
        max_position = None 

        for i, num in enumerate(pontos):
            if num > max_number:
                max_number = num
                max_position = i
        
        maximo.append(max_number)

        pontos_remover = []
        #caso a parte para remover, impossivel criar relação entre novas e remover nos vetores logo casos tem de ser analisados separadametne
        chaves_filtradas_remover = [key for key, value in peca_retirar.items() if value != (0, 0)]
        for chave in chaves_filtradas_remover:
            ponto = bot(nova_pieces[chave], jogador_atual)
            pontos_remover.append(ponto)

        max_number_remover = float('-inf')
        max_position_remover = None 

        for i, num in enumerate(pontos_remover):
            if num > max_number_remover:
                max_number_remover = num
                max_position_remover = i

        maximo.append(max_number_remover) #vetor com 2, maior das casas novas e maior das casas a remover

        if maximo[0] > maximo[1]:
            melhor_peca = chaves_filtradas_nova[max_position]
            print(melhor_peca)
            return melhor_peca

        else:
            melhor_peca = chaves_filtradas_remover[max_position_remover]
            print(melhor_peca)
            return melhor_peca

def generate_random_number():
    return random.randint(1, 5)

def verificar_fim_de_jogo(modo_jogo):
    if modo_jogo == 1:
        if len(preta_pieces) == 0:
            print("O jogador preta venceu! BOT")
            return True
        elif len(branca_pieces) == 0:
            print(f"O jogador branca venceu! {nomes[0]}")
            return True
        else:
            return False
        
    else:
        if len(preta_pieces) == 0:
            print(f"O jogador preta venceu! {nomes[0]}")
            return True
        elif len(branca_pieces) == 0:
            print(f"O jogador branca venceu! {nomes[1]}")
            return True
        else:
            return False

def comecar_jogo(jogador_atual, modo_jogo):
    
    if jogador_atual != ".":
        pass
    else:
        if random.randint(0, 1) == 1:
            jogador_atual = "preta"
        else:
            jogador_atual = "branca"

    game_over = False
    # Loop do Jogo
    modo = modo_jogo
    while not game_over:
        print(f"\nRodada do jogador: {jogador_atual}\n")
        print_tabuleiro()
        peca_imovel = 0
        
        pecas = preta_pieces if jogador_atual == "preta" else branca_pieces

        distancia = generate_random_number()
        print(f"A distância é: {distancia}")
        peca_imovel = testar_condicoes(distancia, jogador_atual, peca_imovel)

        if peca_imovel == len(pecas): 
            pass
        else:
            peca_valida = False
            if distancia == 0:
                pass
            else:
                while not peca_valida:
                    
                    if modo == 1:
                        piece_to_move = peca_mover(jogador_atual)
                    else:
                        piece_to_move = peca_mover_dois()


                    if is_jogador_atual_piece(piece_to_move, jogador_atual):
                        peca_valida = True
                    else:
                        print("Peça inválida. Selecione uma válida.")

                movimento_linha_coluna(piece_to_move, jogador_atual)

        jogador_atual = "branca" if jogador_atual == "preta" else "preta"
        print("---------------------")
        dictionaries = [preta_nova, branca_nova, preta_retirar, branca_retirar]
        for dictionary in dictionaries:
            for key in dictionary:
                dictionary[key] = (0, 0)
        if verificar_fim_de_jogo(modo):
            sair()
        salvar_jogo(jogador_atual, modo_jogo)

def salvar_jogo(jogador_atual, modo_jogo):
    print("Salvar Jogo!")
    try:
        with open("game_save.txt", "w") as file:
            file.write(jogador_atual + "\n")

            preta_pieces_line = "_".join(f"{piece}:{position}" for piece, position in preta_pieces.items())
            file.write(preta_pieces_line + "\n")

            branca_pieces_line = "_".join(f"{piece}:{position}" for piece, position in branca_pieces.items())
            file.write(branca_pieces_line + "\n")

            file.write('%d' % modo_jogo)

            file.write("\n" + nomes[0] + "\n" + nomes[1])

        print("Jogo Salvo!")

    except IOError:
        print("Falha ao salvar o jogo.")

def carregar_jogo():
    try:
        with open("game_save.txt", "r") as file:
            linhas = file.readlines()

        # Remove newline characters and strip leading/trailing whitespaces
        linhas = [line.strip() for line in linhas]
        jogador_atual = linhas[0]

        preta, branca = linhas[1].split("_"), linhas[2].split("_")
        nova_preta, nova_branca = [], []
        for item in preta + branca:
            key, value = item.replace("(", "").replace(")", "").split(":")

            formatted_value = tuple(map(int, value.strip().split(",")))

            if item in preta:
                nova_preta.append(key.strip())
                nova_preta.append(formatted_value)
            else:
                nova_branca.append(key.strip())
                nova_branca.append(formatted_value)

        for i in range(0,len(nova_preta),2):
            preta_pieces[nova_preta[i]] = nova_preta[i+1]

        for i in range(0,len(nova_branca),2):
            branca_pieces[nova_branca[i]] = nova_branca[i+1]

        if linhas[3] == "1":
            nomes[0] = linhas[4]
            comecar_jogo(jogador_atual, 1)
        else:
            nomes[0], nomes[1] = linhas[4], linhas[5]
            comecar_jogo(jogador_atual, 2)

    except IOError:
        print("Falha ao carregar o jogo.")
        sair()

def sair():
    input("Enter para Sair...")
    os.system('cls' if os.name == 'nt' else 'clear')
    exit()

def ver_regras():
    print('''\n\nCada casa só pode ser ocupada por uma única peça e, quando a casa de destino de uma peça está ocupada por uma peça adversária, elas trocam de posição, sendo isso chamado de ataque.
Quando duas peças do mesmo jogador estiverem em uma sequência elas estão protegidas, e não podem ser atacadas.
Quando três peças do mesmo jogador estão em sequência elas formam uma barreira, nenhuma peça adversária pode ultrapassar ou atacá-las. As peças do mesmo jogador podem ultrapassar as suas próprias barreiras.
Se não houver possibilidade de andar com nenhuma das peças a vez é passada ao adversário.
De forma a retirar peças do tabuleiro, o jogador tem de alcançar a Casa da Beleza com um valor exato, não podendo ultrapassar essa casa. Depois de estar na Casa da Beleza, se sair 5 o jogador pode retirar a peça, caso saia 2,3 ou 4 o jogador pode avançar com a peça para uma das últimas 3 casas e caso saia 1, e não tiver mais alternativas de jogo sem ser essa peça, cai na Casa da Humilhação. Depois de entrar nas últimas 3 casas as peças só se mexem se sair o número exato, não podendo trocar entre elas.
''')
    
def escolha_jogo(escolha):
    if escolha == 1:
        try: 
            print("O jogador é as peças Branca\n")
            nomes[1] = input("Nome do Jogador:")
            comecar_jogo(".", 1)
        except ValueError:
            print("Nome Inválida.")
    if escolha == 2:
        print("Jogador 1 - Preta\nJogador 2 - Branca")
        try: 
            nomes[0] = input("Nome do Jogador 1:")
            nomes[1] = input("Nome do Jogador 2:")
            comecar_jogo(".", 2)
        except ValueError:
            print("Nome Inválida.")

def menu_jogo():
    print("1. Jogar contra Bot")
    print("2. Jogar contra outro Jogador")
    try: 
        escolha = int(input("Escolha: "))
        escolha_jogo(escolha)
    except ValueError:
        print("Escolha Inválida.")

def escolha_menu(escolha):
    if escolha == 1:
        menu_jogo()
    elif escolha == 2:
        carregar_jogo()
    elif escolha == 3:
        ver_regras()
    elif escolha == 4:
        sair()
    else:
        print("Escolha Inválida.")

def mostrar_menu():
    print("---------Senet---------\nRealizado por:\nBernardo Almeida al78403 \nVasco Macedo al78798\nTurma Prática 4\n")
    input("Enter para continuar...")

    print("----- Senet Menu -----")
    print("1. Começar Jogo")
    print("2. Carregar Jogo")
    print("3. Ver Regras")
    print("4. Sair")

def main():
    while True:
        try: 
            mostrar_menu()
            choice = int(input("Escolha: "))
            escolha_menu(choice)
        except ValueError:
            print("Escolha Inválida.")

main()