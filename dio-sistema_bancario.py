#SISTEMA BANCÁRIO

# UTILIDADE: CABEÇALHOS E DIVISÕES

def merror(msg):
    print(f"\n\033[1;31m[!] {msg}\033[m\n")

def hr(tipo):
    if tipo == 1:
        print()
        print("\033[1m=\033[m"*47)
        print()

    elif tipo == 2:
        print("-"*47)

def header(msg):
    msg=msg.upper()
    hr(1)
    print(f"\033[1m {msg} \033[m".center(54, " "))
    print()

def msucesso(msg):
    print(f"\033[1m[✓] {msg}\033[m".center(52))
    print()



# OPERAÇÕES BANCÁRIAS

def adicionar_extrato(conta, valor):
    conta["extrato"].append({"data": "00-00-0000", "valor": valor})

    if valor > 0:
        comprovante("Depósito", valor)
    else:
        comprovante("Saque", valor)

def comprovante(tipo, valor):
    hr(1)
    print(f"{tipo} realizado com sucesso!".center(47))
    print(f"Valor: \033[1mR$ {valor:.2f}\033[1m".center(53))

def sacar(conta, limite_transacoes, transacoes_feitas, limite_saque):
    valor_saque = -1

    if transacoes_feitas < limite_transacoes:
        while True:
            print("Informe o valor de saque:")
            print("[i] O saque máximo é de R$ 500,00")
            print("[0] Cancelar operação\n")
                    
            valor_saque = float(input("=> "))

            if valor_saque > 0:

                limite = valor_saque <= limite_saque
                possui_saldo = valor_saque <= conta["saldo"]
                            
                if limite:
                    if possui_saldo:
                        conta["saldo"] -= valor_saque
                        transacoes_feitas += 1
                        adicionar_extrato(
                            conta=conta,
                            valor=-valor_saque, 
                        )
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
                merror("Digite um valor válido!")
                continue

    else:
        print(f"\n\033[1;31m[!] Limite de transações diária atingida ({limite_transacoes}).\nTente novamente amanhã!\033[m")

def depositar(conta, limite_transacoes, transacoes_feitas):
    valor_deposito = -1

    if transacoes_feitas < limite_transacoes:
        while True:
            print("Informe o valor de depósito:\n[0] Cancelar operação\n")
            valor_deposito = float(input("=> "))

            if valor_deposito > 0:
                conta["saldo"] += valor_deposito
                transacoes_feitas += 1
                adicionar_extrato(
                    conta=conta,
                    valor=valor_deposito, 
                )
                break
                    
            elif valor_deposito == 0:
                break

            else:
                merror("Digite um valor válido!")
                continue  

    else:
        print(f"\n\033[1;31m[!] Limite de transações diária atingida ({limite_transacoes}).\nTente novamente amanhã!\033[m")

def exibir_extrato(conta):
    header("SEU EXTRATO BANCÁRIO")
    print(f"\n{'ID':5} {'Data':<12} {'Tipo':<10} {'Valor (R$)':>13}")
    hr(2)

    extrato = conta["extrato"]
    saldo = conta["saldo"]

    for i, dados in enumerate(extrato):
        data = dados['data']
        valor = dados['valor']
        i += 1
        valor_str = ""

        if valor < 0:
            valor_str = f"\033[1;31m{valor:.2f}\033[m"
            print(f"{'%03d' % i:5} {data:<12} {"SAQUE":<10} {valor_str:>23}")
        else:
            valor_str = f"\033[1m{valor:.2f}\033[m"
            print(f"{'%03d' % i:5} {data:<12} {"DEPÓSITO":<10} {valor_str:>20}")

    hr(2)
    print(f"{"Saldo atual:":>31}\033[1m{saldo:>12.2f}\033[m")



# USUÁRIO

def cadastrar_usuario(usuarios, cpf):
    header("CADASTRO")

    print("cpf: ", cpf)
    nome = input("Informe seu nome completo: ")
    nascimento = input("Informe sua data de nascimento (dd-mm-aaaa): ")
    print("Informe seu endereço: ")
    rua = input("Rua: ")
    nro = input("Número: ")
    bairro = input("Bairro: ")
    cidade = input("Cidade: ")
    estado = input("Estado: ")
    endereco = f"{rua}, {nro} - {bairro} - {cidade}/{estado}"

    usuarios.append({"nome": nome.title(), "cpf": cpf, "nascimento": nascimento, "endereco": endereco.title()})

    hr(1)
    msucesso(f"Usuário cadastrado com sucesso!")

def criar_conta(lista_contas, agencia, numero_conta, cpf_usuario, nome):
    lista_contas.append({"agencia": agencia, "numero_conta": numero_conta, "usuario": cpf_usuario, "saldo": 0, "extrato": []})

    hr(1)
    msucesso("Conta criada com sucesso!")
    print(f"{"Agência:":<18} {agencia}")
    print(f"{"Conta corrente:":<18} {numero_conta}")
    print(f"{"Usuário:":<18} {nome}")

def filtrar_usuario(usuarios, cpf):
    usuario_filtrado = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuario_filtrado[0] if usuario_filtrado else None

def menu():
    print('''
[d] Depositar   [s] Sacar    
[e] Extrato     [x] Sair
''')
    return input("=> ")

def selecionar_conta(usuario, contas):
    cpf = usuario['cpf']

    while True:
        lista_contas = [contas_usuario for contas_usuario in contas if contas_usuario["usuario"] == cpf]

        if lista_contas:
            header("Selecione uma conta:")
            hr(2)

            for conta in lista_contas:
                print(f"{"Agência:":<18} {conta["agencia"]}")
                print(f"{"Conta corrente:":<18} {conta["numero_conta"]}")
                print(f"{"Usuário:":<18} {usuario["nome"]}")
                hr(2)

            print("\nDigite o número da conta para entrar:")
            print("[c] Criar uma nova C/C")
            print("[x] Sair\n")

            opcao = input("=> ")
            existe_conta = None

            for conta in lista_contas:
                if str(conta["numero_conta"]) == opcao:
                    existe_conta = conta

            if existe_conta:
                return conta

            elif opcao == "c":
                criar_conta(
                    lista_contas=contas,
                    agencia="0001",
                    numero_conta=len(contas)+1,
                    cpf_usuario=cpf,
                    nome=usuario['nome']
                )

            elif opcao == "x":
                break
                
            else:
                merror("Conta Corrente não existe! Por favor selecione uma conta listada.")     
                           
        else:
            merror("Usuário não possui uma Conta Corrente!") 
            print("Criar conta corrente? [s] Sim [x] Não\n")

            if input("=> ") == 's':
                criar_conta(
                    lista_contas=contas,
                    agencia="0001",
                    numero_conta=len(contas)+1,
                    cpf_usuario=cpf,
                    nome=usuario['nome']
                )
            else:
                break

def conta_usuario(usuario, conta):
    limite_saque = 500
    limite_transacoes = 10

    while True:
        transacoes_feitas = 0

        nome = usuario["nome"].split(" ")
        
        if len(nome) > 1:
            nome = f"{nome[0]} {nome[1]}"
        else:
            nome = usuario["nome"]

        header("Sua conta")
        print(f"Bem vindo, \033[1m{nome}\033[m")
        print(f"Agência: {conta["agencia"]}   C/C: {conta["numero_conta"]}")
        print(f"\nSeu saldo: \033[1mR$ {conta["saldo"]:.2f}\033[m")
        print(f"Transações: {transacoes_feitas}/{limite_transacoes}")
        opcao = menu()
        print()

        if opcao == "d": #DEPÓSITO
            depositar(
                conta=conta, 
                limite_transacoes=limite_transacoes, 
                transacoes_feitas=transacoes_feitas
            )

        elif opcao == "s": #SAQUE
            sacar(
                conta=conta, 
                limite_transacoes=limite_transacoes, 
                transacoes_feitas=transacoes_feitas,
                limite_saque=limite_saque
            )
                
        elif opcao == "e": #EXTRATO
            exibir_extrato(conta=conta)

        elif opcao == "x":
            break

        else:
            print("\033[1;31mOperação inválida, por favor selecione novamente a operação desejada.\033[m")



def main():
    usuarios = []
    contas = []

    usuarios.append({"nome": "Victor Yuri Gomes Cordeiro", "cpf": "61674422318", "nascimento": "15-07-2003", "endereco": None})
    contas.append({"agencia": "0001", "numero_conta": 1, "usuario": "61674422318", "saldo": 0, "extrato": []})

    numero_transacoes = 0
    LIMITE_SAQUE = 500

    while True:
        header("ENTRAR")

        cpf = input("Informe seu CPF (somente números): ")
        usuario = filtrar_usuario(usuarios, cpf)

        if usuario:
            while True:
                conta_selecionada = selecionar_conta(usuario, contas)
                
                if conta_selecionada:
                    conta_usuario(usuario, conta_selecionada)
                else:
                    break

        else:
            merror("Usuário não cadastrado!")
            print("Deseja criar uma conta? [s] Sim  [any key] Não\n")

            criar_usuario = input("=> ")
            print()

            if criar_usuario == "s":
                cadastrar_usuario(usuarios, cpf)

main()