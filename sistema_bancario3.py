from abc import ABC, ABCMeta, abstractclassmethod, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self, conta, transacao, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(conta=None, transacao=None, endereco=endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente,):
        self._saldo = 0 
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente 
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
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
        saldo = self.saldo
        excedeu_saldo =  valor > saldo

        if excedeu_saldo:
            print("Você não tem saldo suficiente")

        elif valor > 0:
            self._saldo -= valor
            print("Saque realizado com sucesso!")
            return True
        
        else:
            print("O valor inserido não é um valor valido.")
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Deposito realizado com sucesso!")
        else:
            print("O valor inserido não é um valor valido.")

        return True
    
class Conta_corrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
    
    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("O valor inserido não é um valor valido.")
        
        elif excedeu_saques:
            print("Numero maximo de saques excedido.")

        else:
            return super().sacar(valor)
        return False

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),  
            }
        )
    
class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._value
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


menu = """

[1] Sacar
[2] Depositar
[3] Extrato
[4] Cadastrar Usuário
[5] Criar uma nova Conta
[0] Sair

=>"""

def main():
    clientes = []
    contas = []

    while True:
        opcao = input(menu)

        if opcao == "2":
            depositar(clientes)

        if opcao == "1":
            sacar(clientes)
        
        elif opcao == "3":
            exibir_extrato(clientes)
        
        elif opcao == "4":
            criar_clientes(clientes)
        
        elif opcao == "5":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        
        elif opcao == "0":
            break

def depositar(clientes):
    cpf = input("Informe seu CPF:")
    cliente =  filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não cadastrado.")
        return
    
    valor = float(input("Informe o valor de depósito:"))

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        print("Cliente precisa criar uma conta antes de depositar!")
        return
    
    conta.depositar(valor)

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui uma conta!")
        return False
    return cliente.contas[0]

def sacar(clientes):
    cpf = input("Informe o seu CPF")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado")
        return
    
    valor = float(input("Informe o valor de saque:"))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe seu CPF:")
    cliente =  filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    print("=======EXTRATO=======")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("=========================================")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe seu CPF:")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado")
        return
    
    conta = Conta_corrente.nova_conta(cliente=cliente, numero=numero_conta)
    cliente.adicionar_conta(conta)
    contas.append(conta)

    print("\n Conta criada com sucesso!")

def listar_contas(contas):
    for conta in contas:
        print("=" + 100)

def criar_clientes(clientes):
    cpf = input("Informe seu CPF:")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("Ja existe cliente cadastrado com CPF:")
        return
    
    nome = input("Informe o nome completo:")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaa): *")
    endereco = input("Informe o endereço (logradouro, nro -  bairro - cidade/sigla estado): *")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n Cliente criado com sucesso!")

main()
