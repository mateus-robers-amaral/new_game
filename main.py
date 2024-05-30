import time
import csv
import sys

lista_npcs = []
player = { "nome" : "Mateus",
          "level": 1,
          "exp" : 0,
          "exp_max" : 50,
          "hp" : 100,
          "hp_max" : 100,
          "dano" : 25,
          "moedas" : 5,
}

def criar_npc(level):

    novo_npc = {
        "nome" : f"Monstro {level}",
        "level" : level,
        "dano" : 5 * level,
        "hp" : 100 * level,
        "hp_max" : 100 * level,
        "exp" : 7 * level,
    }

    return novo_npc

def gerar_npc(n_npcs):
    for i in range(n_npcs):
        npc = criar_npc(i + 1)
        lista_npcs.append(npc)

def exibir_npcs():
    for npc in lista_npcs:
        exibir_npc(npc)

def exibir_npc(npc):
    print(f"Nome: {npc['nome']} | Level: {npc['level']} | Dano: {npc['dano']} | HP: {npc['hp']} / {npc['hp_max']}")

def exibir_player():
    print(f"Nome: {player['nome']} | Level: {player['level']} | Dano: {player['dano']} | HP: {player['hp']} / {player['hp_max']} | EXP: {player['exp']}/{player['exp_max']} | Moedas: {player['moedas']}\n")

def dinheiro():
    with open('RPG/historias/conto_da_floresta.csv', mode='+a') as arquivo:
        escrior_csv = csv.writer(arquivo)
        escrior_csv.writerow(str(player['moedas']))

def cura():
    try:
        print("Qual poção deseja comprar?\n[1] Pequena\n[2] Média\n[3] Grande")
        resp = int(input("-> "))
        if resp == 1:
            if player['hp'] == player['hp_max']:
                print(f"\n{player['nome']} já está com a vida cheia!\n")
            else:
                player['hp'] += 5
        elif resp == 2:
            if player['hp'] == player['hp_max']:
                print(f"\n{player['nome']} já está com a vida cheia!\n")
            else:
                player['hp'] += 10
        elif resp == 3:
            if player['hp'] == player['hp_max']:
                print(f"\n{player['nome']} já está com a vida cheia!\n")
            else:
                player['hp'] += 20
        elif resp == 4:
            time.sleep(2)
            print("\nHm...?")
            time.sleep(2)
            print("\nParabéns! Você invocou a poção fantástica\nReceba cura total!\n")
            player['hp'] = player['hp_max']

        else:
            print("Opção inválida!\n")
            return False
            
    except ValueError:
        print("Opção inválida!\n")
        return False

    exibir_player()

def descanso():
    try:
        dia = 1
        print("1 dia de descanso regenera 5 de hp!")
        resp = int(input("Quantos dias deseja descansar?\n-> "))
        while dia <= resp:
            print(f"Você está no {dia}° dia de descanso e está com {player['hp']}/{player['hp_max']} de vida.")
            dia += 1
            player['hp'] += 5
            if player['hp'] <= player['hp_max']:
                time.sleep(2)
                print("\nzZz\n")
                time.sleep(2)
                continue
            else:
                print("\nHora de acordar!\n")
                break
    
    except ValueError:
        print("Opção inválida!\n")
        return False

def armas():
    try:
        print("Qual arma deseja comprar?\n\n[1] Adaga\n[2] Espada\n[3] Arco")
        compra = int(input("-> "))
        print()
        if compra == 1:
            player['dano'] += 5
            exibir_player()
        elif compra == 2:
            player['dano'] += 10
            exibir_player()
        elif compra == 3:
            player['dano'] += 15
            exibir_player()
        elif compra == 77:
            time.sleep(2)
            print("\nHm...?\n")
            time.sleep(2)
            print("Você roubou o cajado do Mago Mercante e desbloqueou um poder supremo!\n")
            player['dano'] += 77
            exibir_player()

    except ValueError:
        print("Opção inválida!\n")
        return False

def reset_npc(npc):
    npc['hp'] = npc['hp_max']

def mago():
    try:
        while True:
            print("Olá viajante!\nSou o Mago Mercante e trago bons prdutos para sua aventura!\n")
            compra = int(input("O que deseja comprar hoje?\n[1] Poções de Cura\n[2] Armas de Batalha\n-> "))
            if compra == 1:
                cura()
                break
            elif compra == 2:
                armas()
                break
            else:
                print("Escolha uma opção válida!\n")
                continue
    except ValueError:
        print("Opção inválida!\n")
        return False

def level_up():
    if player['exp'] >= player['exp_max']:
        player['level'] += 1
        player['exp'] = 0
        player['exp_max'] = player['exp_max'] * 2
        player['hp_max'] += 20
        player['dano'] += 5
        print(f"\nParabéns {player['nome']}, você subiu de level!\nNovo level: {player['level']}")

def iniciar_batalha(npc):
    while player['hp'] > 0 and npc['hp'] > 0:
        atacar_npc(npc)
        print("⚔️\n")
        time.sleep(1)
        atacar_player(npc)
        print("⚔️\n")
        time.sleep(1)
        exibir_info_batalha(npc)

    if player['hp'] > 0:
        print(f"{player['nome']} venceu e ganhou {npc['exp']} de EXP!\n")
        player['exp'] += npc['exp']
        exibir_player()
        time.sleep(1)

        try:
            print("\nDeseja se curar?\n[1] Sim\n[2] Não")
            resp = int(input("-> "))
            print()
            if resp == 1:
                print("[1] Poções\n[2] Descansar")
                resp = resp = int(input("-> "))
                print()
                if resp == 1:
                    cura()
                elif resp == 2:
                    descanso()
            elif resp == 2:
                pass
        except ValueError:
            print("Opção inválida!\n")
            return False

        level_up()
        reset_npc(npc)

    else:
        print(f"O {npc['nome']} venceu!")
        morte()
        exibir_npc(npc)

def atacar_player(npc):
    player["hp"] -= npc["dano"]

def atacar_npc(npc):
    npc["hp"] -= player["dano"]

def exibir_info_batalha(npc):
    print(f"Player: {player['hp']} / {player['hp_max']}")
    print(f"{npc['nome']}: {npc['hp']} / {npc['hp_max']}")
    print("-------------------------\n")

def morte():
    try:
        print(f"\n{player['nome']} morreu, e precisa ser curado para continuar jogando!\n")
        resp = int(input(f"Deseja ressucitar {player['nome']}?\n[1] Sim\n[2] Não\n-> "))
        if resp == 1:
            cura()
        elif resp == 2:
            sys.exit()
    
    except ValueError:
        print("Opção inválida!\n")
        return False

# função geradora de monstros        
gerar_npc(15)
#exibir_npcs()
dinheiro()


def main():
    try:
        contador = 0
        print("O que deseja fazer agora??\n")
        resp = int(input("[1] Continuar explorando\n[2] Batalhar contra um monstro\n[3] Conversar com o Mago Mercante\n-> "))
        print()
        if resp == 1:
            time.sleep(1)
            print("Era uma vez...\n")
            time.sleep(1)
            print("Até que...\n")
            #colocar em uma lista
            historia = str(input("\nPor onde começa a sua história?\n-> "))
            historia.replace(',', ' ')
            with open('RPG/historias/conto_da_floresta.csv', mode='a', newline="") as arquivo:
                escritor_csv = csv.writer(arquivo)
                escritor_csv.writerow(historia)
            print()


            # with open('RPG/historias/conto_da_floresta.csv', mode= 'r') as file:
            #     leitor_csv = csv.reader(file)
            #     for linha in leitor_csv:
            #         print(linha[0])  
            time.sleep(1)
            main()
        elif resp == 2:
            duelo = int(input("Quantos duelos deseja fazer?\n-> "))
            selec = int(input("\nQual nível de npc deseja bastalhar?\n-> "))
            if selec == 1:
                npc_selecionado = lista_npcs[0]
            elif selec == 2:
                npc_selecionado = lista_npcs[1]
            elif selec == 3:
                npc_selecionado = lista_npcs[2]
            elif selec == 4:
                npc_selecionado = lista_npcs[3]
            elif selec == 5:
                npc_selecionado = lista_npcs[4]
            elif selec == 6:
                npc_selecionado = lista_npcs[5]
            elif selec == 7:
                npc_selecionado = lista_npcs[6]
            elif selec == 8:
                npc_selecionado = lista_npcs[7]
            elif selec == 9:
                npc_selecionado = lista_npcs[8]
            elif selec == 10:
                npc_selecionado = lista_npcs[9]
            elif selec == 11:
                npc_selecionado = lista_npcs[10]
            elif selec == 12:
                npc_selecionado = lista_npcs[11]
            elif selec == 13:
                npc_selecionado = lista_npcs[12]
            elif selec == 14:
                npc_selecionado = lista_npcs[13]
            elif selec == 15:
                npc_selecionado = lista_npcs[14]
            elif selec == 2:
                npc_selecionado = lista_npcs[15]

            while contador != duelo:
                contador += 1
                iniciar_batalha(npc_selecionado)
                print()
            time.sleep(1)
            main()
                
        elif resp == 3:
            mago()
            time.sleep(1)
            main()
    
    except ValueError:
        print("Opção inválida!\n")
        return False

main()