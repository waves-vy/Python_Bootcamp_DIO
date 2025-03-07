from abc import ABC, abstractmethod, abstractproperty
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
    print()
    hr(1)
    print()
    print(f"\033[1m[✓] {msg}\033[m".center(largura+5))

def header(msg):
    msg=msg.upper()
    print("\n")
    print(f" \033[1;47m {msg} \033[m ".center(largura+10,"="))
    print("\n")

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



class Cliente:
    def __init__(self, cpf, nome, data_nascimento, endereco):
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)
    
class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(cpf, nome, data_nascimento, endereco)

class PessoaJuridica(Cliente):
    pass



class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 1000
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod #Fábrica de classes
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente
        
    @property
    def historico(self):
        return self._historico 

    def sacar(self, valor):
        self._saldo -= valor
        transacao = self._historico.adicionar_transacao(-valor)
        comprovante(transacao, self)

    def depositar(self, valor):
        self._saldo += valor
        transacao = self._historico.adicionar_transacao(valor)
        comprovante(transacao, self)

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, saque_max=500, limite_diario=3):
        super().__init__(numero,cliente)
        self.saque_max = saque_max
        self.limite_diario = limite_diario
        self.tipo = ("CC", "Conta Corrente")



class Transacao:
    def __init__(self):
        self._contagem_transacoes = 0

    @property
    def limite_diario(self):
        historico = self._conta.historico.transacoes
        self._contagem_transacoes = 0
        hoje = date.today().strftime("%d/%m/%y")

        for transacao in historico:
            data_transacao = transacao["data_hora"].split(" ")
            if data_transacao[0] == hoje:
                self._contagem_transacoes += 1

        return self._contagem_transacoes

    def sacar(self, conta, valor):
        self._conta = conta
        limite_diario = self.limite_diario < self._conta.limite_diario
        limite_saque = valor <= self._conta.saque_max

        if limite_diario:
            if valor > 0:
                if limite_saque:
                    if valor <= self._conta.saldo:
                        self._conta.sacar(valor)
                        return True
                    else:
                        merror("Saldo insuficiente.")
                        return False
                
                else:
                    merror(f"O valor limite de saque é R$ {self._conta.saque_max:.2f}. Reduza o valor!")
                    return False
                
            elif valor == 0:
                return True
            
            else:
                merror("Digite um valor válido!")
                return False       
        else:
            merror(f"Limite de transações diária atingida ({self._conta.limite_diario})!")
            return True

    def depositar(self, conta, valor):
        self._conta = conta
        limite_diario = self.limite_diario < self._conta.limite_diario

        if limite_diario:
            if valor > 0:
                self._conta.depositar(valor)
                return True
            elif valor == 0:
                return True
            else:
                merror("Digite um valor válido!")
                return False       
        else:
            merror(f"Limite de transações diária atingida ({self._conta.limite_diario})!")
            return True

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, valor):
        data_hora = datetime.now().strftime("%d/%m/%y %H:%M:%S")
        transacao = {"data_hora": data_hora, "valor": valor}
        self._transacoes.append(transacao)
        return transacao



def transacao(conta, tipo):
    while True:
        if tipo == "s":
            operacao = "saque"
        else:
            operacao = "depósito"

        header(operacao)
        print("Insira o valor:")
        print("[0] Cancelar operação\n")
                    
        valor = float(input("=> "))

        if tipo == "s":
            transacao = Transacao().sacar(conta, valor)
        else:
            transacao = Transacao().depositar(conta, valor)
        
        if transacao:
            break
    
def exibir_extrato(conta):
    header("SEU EXTRATO BANCÁRIO")

    printjus((f"[{conta.tipo[0]}]", conta.tipo[1]))
    printjus((f"Cliente:", conta.cliente.nome))
    printjus((f"CPF: {conta.cliente.cpf}",
            f"Agência: {conta.agencia}",
            f"N: {conta.numero}"
    ))     

    print(f"\n\033[1m{'ID':3} {'Data':<8} {'Hora':<10} {'Tipo':<10} {'Valor (R$)':>15}\033[m")
    hr(2)

    extrato = conta.historico.transacoes
    saldo = conta.saldo

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
    print()

    hoje = datetime.now().strftime("%d/%m/%y %H:%M:%S")
    print(f"Extrato gerado em: {hoje}")

def comprovante(transacao, conta):
    tipo = ""
    if transacao["valor"] > 0:
        tipo = "Depósito"
    else:
        tipo = "Saque"

    msucesso(f"{tipo} realizado com sucesso!")
    print()
    hr(2)

    h2(f"COMPROVANTE DE {tipo.upper()}")


    data_hora = transacao["data_hora"].split(" ")
    data = data_hora[0]
    hora = data_hora[1]

    printjus((f"[{conta.tipo[0]}]", conta.tipo[1]))
    printjus((f"CPF: {conta.cliente.cpf}",
                f"Agência: {conta.agencia}",
                f"Número: {conta.numero}"))
        
    printjus((f"Cliente: ", conta.cliente.nome))
    print()
    printjus((f"Valor: R$ {abs(transacao["valor"]):.2f}", data, hora))



def cadastrar_cliente(clientes):
    header("CADASTRO")
    
    print("Informe os seguintes dados:\n")

    while True:
        cpf = input(f"CPF: ")
        if cpf:
            break

    lista_cpf = [cliente.cpf for cliente in clientes]
    filtra_cpf = lista_cpf.count(cpf)

    if not filtra_cpf:
        d = { #key : #input
            "nome": "Nome completo: ",
            "data_nascimento": "Data de nascimento (dd/mm/aaaa): ",
            "rua": "Endereço\nRua: ",
            "nro": "Número: ",
            "complemento": "Complemento: ",
            "bairro": "Bairro: ",
            "cidade": "Cidade: ",
            "estado": "Estado (sigla): ",
        }

        for pergunta in d:
            while True:
                resposta = input(d[pergunta])
                if resposta:
                    d[pergunta] = resposta.upper()
                    break

        endereco = f"{d["rua"]}, {d["nro"]}, {d["complemento"]} - {d["bairro"]} - {d["cidade"]}/{d["estado"]}".upper()

        cliente = PessoaFisica(cpf=cpf, nome=d["nome"], data_nascimento=d["data_nascimento"], endereco=endereco)
        clientes.append(cliente)
            
        msucesso("Usuário cadastrado com sucesso!")
    else:
        merror("CPF já é cadastrado.")

def filtrar_cliente(clientes, cpf):
    cliente_filtrado = [cliente for cliente in clientes if cliente.cpf == cpf]
    return cliente_filtrado[0] if cliente_filtrado else None



def criar_conta(cliente, contas):
    while True:
        header("Criar Conta")
        print("""Que tipo de conta deseja abrir?
              
[CC] Conta Corrente
[PJ] Conta Empresarial (em breve...)
 [X] Sair
""")    
        numero = len(contas) + 1
        tipo_conta = input("=> ").upper()

        if tipo_conta == "CC":
            conta = ContaCorrente.nova_conta(numero, cliente)
            cliente.adicionar_conta(conta)
            contas.append(conta)

            msucesso("Conta criada com sucesso!")
            print()

            print(f"Tipo:\t Conta Corrente")
            print(f"Agência: {conta.agencia}   Numero: {conta.numero}")
            print(f"Cliente: {cliente.nome}")
            break

        elif tipo_conta == "PJ":
            merror("Opção indisponível.")

        elif tipo_conta == "X":
            break
            
        else:
            merror("Opção indisponível.")

def selecionar_conta(cliente, contas):
    while True:
        lista_contas = cliente.contas

        if lista_contas:
            header("Selecione uma conta")

            hr(2)
            for i, conta in enumerate(lista_contas):
                print(f"\t{cliente.nome.title()}")
                print(f"  [{i+1}]\tAgência: {conta.agencia}\t{conta.tipo[0]}: {conta.numero}")
                print(f"\t{conta.tipo[1]}")
                hr(2)

            print("\nSelecione uma conta:")
            print("[c] Criar uma nova conta")
            print("[x] Sair\n")

            opcao = input("=> ")

            if opcao <= str(len(lista_contas)) and not opcao <= '0':
                i = int(opcao)-1
                return lista_contas[i]

            elif opcao == "c":
                criar_conta(cliente, contas)

            elif opcao == "x":
                break
                
            else:
                merror("Selecione uma conta listada!")     
                           
        else:
            criar_conta(cliente, contas)



def main():
    clientes = []
    contas = []

    LIMITE_SAQUE = 500

    while True:
        header("ENTRAR")

        cpf = input("Informe seu CPF (somente números): ")
        
        if len(cpf) == 11:
            cliente = filtrar_cliente(clientes, cpf)
        else:
            merror("CPF inválido!")
            continue

        if cliente:
            while True:
                conta = selecionar_conta(cliente, contas)
                
                if conta:
                    conta_usuario(conta)
                else:
                    break

        else:
            merror("Usuário não cadastrado!")
            print("Deseja criar um cadastro? [s] Sim  [any key] Não\n")

            criar_usuario = input("=> ")

            if criar_usuario == "s":
                cadastrar_cliente(clientes)

def menu():
    print('''
[d] Depositar   [s] Sacar    
[e] Extrato     [x] Sair
''')
    return input("=> ")

def conta_usuario(conta):
    while True:
        nome = conta.cliente.nome.split(" ")
        
        if len(nome) > 1:
            nome = f"{nome[0]} {nome[1]}"
        else:
            nome = conta.cliente.nome

        header("Sua conta")
        print(f"Bem vindo, \033[1m{nome.title()}\033[m")
        print(f"Agência: {conta.agencia}   N: {conta.numero}")
        print(f"\nSeu saldo: \033[1mR$ {conta.saldo:.2f}\033[m")
        opcao = menu()

        if opcao == "d": #DEPÓSITO
            transacao(conta, "d")

        elif opcao == "s": #SAQUE
            transacao(conta, "s")
                                    
        elif opcao == "e": #EXTRATO
            exibir_extrato(conta)

        elif opcao == "x":
            break

        else:
            merror("Operação indisponível.")

main()