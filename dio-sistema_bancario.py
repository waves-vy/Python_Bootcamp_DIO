from datetime import datetime, date

# FORMATAÇÃO
largura = 50

def printjus(msg, distancia=largura):
    if len(msg) > 1:
        for conjunto in msg:
            distancia -= len(conjunto)

        distancia = distancia // (len(msg) - 1)
        msg_str = ""

        for i, conjunto in enumerate(msg):
            msg_str += conjunto
            if i < len(msg):
                msg_str += (" "*distancia)

        print(msg_str)

def merror(msg):
    print(f"\n\033[1;31m[!] {msg}\033[m\n")

def msucesso(msg):
    print(f"\033[1m[✓] {msg}\033[m".center(largura+5))
    print()

def header(msg):
    msg=msg.upper()
    hr(1)
    print(f"\033[1m{msg}\033[m".center(largura+5))
    print()

def h2(msg):
    print()
    print(f"{msg.upper()}".center(largura))
    print()

def hr(tipo):
    if tipo == 1:
        print()
        print("\033[1m=\033[m"*largura)
        print()

    elif tipo == 2:
        print("-"*largura)



# OPERAÇÕES BANCÁRIAS
def qtd_transacoes_hoje(extrato):
    transacoes_hoje = 0
    hoje = date.today().strftime("%d/%m/%y")

    for transacao in extrato["extrato"]:
        data_transacao = transacao["data_hora"].split(" ")
        if data_transacao[0] == hoje:
            transacoes_hoje += 1

    return transacoes_hoje

def adicionar_extrato(conta, valor, cliente, transacoes):
    data_hora = datetime.now().strftime("%d/%m/%y %H:%M:%S")
    conta["extrato"].append({"data_hora": data_hora, "valor": valor})
    tipo = "Depósito" if valor > 0 else "Saque" 
    comprovante(conta, cliente, tipo, valor, data_hora, transacoes)

def comprovante(conta, cliente, tipo, valor, data_hora, transacoes):
    hr(1)
    msucesso(f"{tipo} realizado com sucesso! [{transacoes[0]+1}/{transacoes[1]}]")
    hr(2)

    h2(f"COMPROVANTE DE {tipo}")

    data_hora = data_hora.split(" ")
    data = data_hora[0]
    hora = data_hora[1]

    printjus((
        f"CPF: {cliente["cpf"]}",
        f"Agência: {conta["agencia"]}",
        f"C/C: {conta["numero_conta"]}"
    ))
    printjus(("Cliente:", f"{cliente["nome"]}"))
    print()
    printjus((f"Valor: R$ {valor:.2f}", data, hora))

def sacar(conta, cliente, limite_transacoes, limite_saque):
    valor_saque = -1

    transacoes_feitas = qtd_transacoes_hoje(conta)

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
                        adicionar_extrato(
                            conta=conta,
                            cliente=cliente,
                            valor=-valor_saque, 
                            transacoes=(transacoes_feitas, limite_transacoes)
                        )
                        return 1

                    else:
                        merror("Saldo insuficiente")
                        continue

                else:
                    merror(f"O valor limite por saque é R$ {limite_saque:.2f}. Reduza o valor!")
                    continue
                        
            elif valor_saque == 0:
                return 0

            else:
                merror("Digite um valor válido!")
                continue

    else:
        print(f"\n\033[1;31m[!] Limite de transações diária atingida ({limite_transacoes}).\nTente novamente amanhã!\033[m")
        return 0

def depositar(conta, cliente, limite_transacoes):
    valor_deposito = -1
    transacoes_feitas = qtd_transacoes_hoje(conta)

    if transacoes_feitas < limite_transacoes:
        while True:
            print("Informe o valor de depósito:\n[0] Cancelar operação\n")
            valor_deposito = float(input("=> "))

            if valor_deposito > 0:
                conta["saldo"] += valor_deposito
                adicionar_extrato(
                    conta=conta,
                    cliente=cliente,
                    valor=valor_deposito,
                    transacoes=(transacoes_feitas, limite_transacoes) 
                )
                return 1
                    
            elif valor_deposito == 0:
                return 0

            else:
                merror("Digite um valor válido!")
                continue  

    else:
        merror(f"Limite de transações diária atingida ({limite_transacoes}).\nTente novamente amanhã!")
        return 0

def exibir_extrato(conta, usuario):
    header("SEU EXTRATO BANCÁRIO")

    printjus((f"Cliente:", usuario["nome"]))
    printjus((f"CPF: {usuario["cpf"]}",
                f"Agência: {conta["agencia"]}",
                f"C/C: {conta["numero_conta"]}"
    ))     

    print(f"\n\033[1m{'ID':3} {'Data':<8} {'Hora':<10} {'Tipo':<10} {'Valor (R$)':>15}\033[m")
    hr(2)

    extrato = conta["extrato"]
    saldo = conta["saldo"]

    for i, dados in enumerate(extrato):
        data = dados["data_hora"]
        valor = dados["valor"]
        i += 1

        valor_str = ""
        tipo = ""

        if valor < 0:
            valor_str = f"\033[1;31m{valor:.2f}\033[m"
            print(f"{'%02d' % i:3} {data:<19} {"SAQUE":<10} {valor_str:>25}")
        else:
            valor_str = f"\033[1m{valor:.2f}\033[m"
            print(f"{'%02d' % i:3} {data:<19} {"DEPÓSITO":<10} {valor_str:>22}")

    hr(2)
    print(f"{"Saldo atual:":>31}\033[1m{saldo:>19.2f}\033[m")



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
                return existe_conta

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
        nome = usuario["nome"].split(" ")
        
        if len(nome) > 1:
            nome = f"{nome[0]} {nome[1]}"
        else:
            nome = usuario["nome"]

        header("Sua conta")
        print(f"Bem vindo, \033[1m{nome}\033[m")
        print(f"Agência: {conta["agencia"]}   C/C: {conta["numero_conta"]}")
        print(f"\nSeu saldo: \033[1mR$ {conta["saldo"]:.2f}\033[m")
        opcao = menu()
        print()

        if opcao == "d": #DEPÓSITO
            depositar(
                conta=conta, 
                cliente=usuario,
                limite_transacoes=limite_transacoes
            )

        elif opcao == "s": #SAQUE
            sacar(
                conta=conta, 
                cliente=usuario,
                limite_transacoes=limite_transacoes, 
                limite_saque=limite_saque
            )
                                    
        elif opcao == "e": #EXTRATO
            exibir_extrato(conta=conta, usuario=usuario)

        elif opcao == "x":
            break

        else:
            print("\033[1;31mOperação inválida, por favor selecione novamente a operação desejada.\033[m")



def main():
    usuarios = []
    contas = []

    usuarios.append({"nome": "Victor Yuri Gomes Cordeiro", "cpf": "61674422318", "nascimento": "15-07-2003", "endereco": None})
    contas.append({"agencia": "0001", "numero_conta": 1, "usuario": "61674422318", "saldo": 0, "extrato": []})

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
            print("Deseja criar um cadastro? [s] Sim  [any key] Não\n")

            criar_usuario = input("=> ")
            print()

            if criar_usuario == "s":
                cadastrar_usuario(usuarios, cpf)

main()