#SISTEMA BANCÁRIO

menu = '''
[d] Depositar   [s] Sacar    
[e] Extrato     [q] Sair

=> '''

saldo = 0
extrato = []
numero_transacoes = 0
LIMITE_SAQUE = 500



# OPERAÇÕES

def adicionar_extrato(*transacao):
    global extrato
    extrato.append(transacao)

def comprovante(tipo, valor):
    print()
    print("="*40)
    print()

    print(f"{tipo} realizado com sucesso!".center(40))
    print(f"Valor: \033[1mR$ {valor:.2f}\033[1m".center(47))

def sacar(limite_saque, limite_transacoes):
    global saldo
    global numero_transacoes

    valor_saque = -1
    
    if numero_transacoes < limite_transacoes:
        while True:
            print("Informe o valor de saque:")
            print("[i] O saque máximo é de R$ 500,00")
            print("[0] Cancelar operação\n")
                    
            valor_saque = float(input("=> "))

            if valor_saque > 0:

                limite = valor_saque <= limite_saque
                possui_saldo = valor_saque <= saldo
                            
                if limite:
                    if possui_saldo:
                        saldo -= valor_saque
                        numero_transacoes += 1
                        adicionar_extrato("SAQUE", valor_saque)
                        comprovante("Saque", valor_saque)
                        break

                    else:
                        print("\n\033[1;31mSaldo insuficiente.\033[m\n")
                        continue

                else:
                    print(f"\n\033[1;31m[!] O valor limite por saque é R$ {limite_saque:.2f}. Reduza o valor!\033[m\n")
                    continue
                        
            elif valor_saque == 0:
                break

            else:
                print("\n\033[1;31m[!] Digite um valor válido!\033[m\n")
                continue

    else:
        print(f"\n\033[1;31m[!] Limite de transações diária atingida ({limite_transacoes}).\nTente novamente amanhã!\033[m")

def depositar(limite_transacoes):
    global saldo
    global numero_transacoes

    valor_deposito = -1

    if numero_transacoes < limite_transacoes:
        while True:
            print("Informe o valor de depósito:\n[0] Cancelar operação\n")
            valor_deposito = float(input("=> "))

            if valor_deposito > 0:
                saldo += valor_deposito
                numero_transacoes += 1
                adicionar_extrato("DEPÓSITO", valor_deposito)
                comprovante("Depósito", valor_deposito)
                break
                    
            elif valor_deposito == 0:
                break

            else:
                print("\n\033[1;31m[!] Digite um valor válido!\033[m\n")
                continue  

    else:
        print(f"\n\033[1;31m[!] Limite de transações diária atingida ({limite_transacoes}).\nTente novamente amanhã!\033[m")

def exibir_extrato(extrato):
    print("\033[1m SEU EXTRATO BANCÁRIO \033[m".center(47, "="))
    print(f"\n{'ID':4}  {'Tipo':<10}  {'Valor (R$)':>13}")
    print("-".center(40, '-'))

    for i, (type, value) in enumerate(extrato):
        i += 1
        value_str = ""

        if type == "SAQUE":
            value_str = f"\033[1;31m-{value:.2f}\033[m"
            print(f"{'%03d' % i:4}  {type:<10}  {value_str:>23}")
        else:
            value_str = f"\033[1m{value:.2f}\033[m"
            print(f"{'%03d' % i:4}  {type:<10}  {value_str:>20}")

    print("-".center(40, '-'))
    print(f"Saldo atual:\033[1m{saldo:>19.2f}\033[m")



# INTERFACE

while True:

    print()
    print("\033[1m SUA CONTA \033[m".center(47, "="))
    print(f"\nSeu saldo: \033[1mR$ {saldo:.2f}\033[m")
    opcao = input(menu)
    print()

    if opcao == "d": #DEPÓSITO
        depositar(limite_transacoes=10)

    elif opcao == "s": #SAQUE
        sacar(limite_saque=500, limite_transacoes=10)
            
    elif opcao == "e": #EXTRATO
        exibir_extrato(extrato)

    elif opcao == "q":
        break

    else:
        print("\033[1;31mOperação inválida, por favor selecione novamente a operação desejada.\033[m")