#SISTEMA BANCÁRIO

menu = '''
[d] Depositar   [s] Sacar    
[e] Extrato     [q] Sair

=> '''

saldo = 0
limite = 500
extrato = []
numero_saques = 0
LIMITE_SAQUES = 3

def adicionar_extrato(*transacao):
    global extrato
    extrato.append(transacao)

def transacao_realizada(tipo, valor):
    print()
    print("="*40)
    print()

    print(f"{tipo} realizado com sucesso!".center(40))
    print(f"Valor: \033[1mR$ {valor:.2f}\033[1m".center(47))

while True:

    print()
    print("\033[1m SUA CONTA \033[m".center(47, "="))
    print(f"\nSeu saldo: \033[1mR$ {saldo:.2f}\033[m")

    opcao = input(menu)

    print()

    if opcao == "d":

        valor_deposito = -1

        while valor_deposito != 0:
            print("Informe o valor de depósito:\n[0] Cancelar operação\n")
            valor_deposito = float(input("=> "))

            if valor_deposito > 0:
                saldo += valor_deposito
                adicionar_extrato("DEPÓSITO", valor_deposito)
                transacao_realizada("Depósito", valor_deposito)
                break
                
            elif valor_deposito == 0:
                break

            else:
                print("\n\033[1;31m[!] Digite um valor válido!\033[m\n")
                continue  

    elif opcao == "s":

        limite_diario = numero_saques < LIMITE_SAQUES

        if limite_diario:

            valor_saque = -1

            while valor_saque != 0:
                print("Informe o valor de saque:")
                print("[i] O saque máximo é de R$ 500,00")
                print("[0] Cancelar operação\n")
                
                valor_saque = float(input("=> "))

                if valor_saque > 0:

                    limite_saque = valor_saque <= limite
                    possui_saldo = valor_saque <= saldo
                    
                    if limite_saque:
                        if possui_saldo:
                            saldo -= valor_saque
                            numero_saques += 1
                            adicionar_extrato("SAQUE", valor_saque)
                            transacao_realizada("Saque", valor_saque)
                            break

                        else:
                            print("\n\033[1;31mSaldo insuficiente.\033[m\n")
                            continue

                    else:
                        print(f"\n\033[1;31m[!] O valor limite por saque é R$ {limite:.2f}. Reduza o valor!\033[m\n")
                        continue
                
                elif valor_saque == 0:
                    break

                else:
                    print("\n\033[1;31m[!] Digite um valor válido!\033[m\n")
                    continue

        else:
            print("\n\033[1;31m[!] Limite de saques diário atingido (3).\nTente novamente amanhã!\033[m")


    elif opcao == "e":
        print("\033[1m SEU EXTRATO BANCÁRIO \033[m".center(47, "="))
        print("\nID    Tipo          Valor (R$)\n")

        i = 0

        for type, value in extrato:
            i += 1
            value_str = ""

            if type == "SAQUE":
                value_str = f"\033[1;31m-{value:.2f}\033[m"
                print(f"{'%02d' % i:5} {type:<10} {value_str:>23}")
            else:
                value_str = f"\033[1m{value:.2f}\033[m"
                print(f"{'%02d' % i:5} {type:<10} {value_str:>20}")

        print(f"\nSaldo atual: R$ \033[1m{saldo:.2f}\033[m")

    elif opcao == "q":
        break

    else:
        print("\033[1;31mOperação inválida, por favor selecione novamente a operação desejada.\033[m")