menu = """

[1] Sacar
[2] Depositar
[3] Extrato
[4] Cadastrar Usuário
[5] Criar uma nova Conta
[0] Sair

=>"""

def main():
    AGENCIA = "0001"
    MAX_SAQUES = 3
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = input(menu)

        if opcao == "2":
            print("Depositar")
            valor = int(input("Informe o Valor de Deposito:"))
            saldo, extrato = Depositar(saldo, extrato, valor)

        elif opcao == "1":
            print("Sacar")
            valor = int(input("Informe o Valor de Saque:"))
            saldo, extrato, numero_saques = sacar(saldo=saldo, valor=valor, numero_saques=numero_saques, MAX_SAQUES=MAX_SAQUES, limite=limite, extrato=extrato)

        elif opcao == "3":
           Extrato(saldo, extrato=extrato)

        elif opcao == "4":
            cad_usuario(usuarios)

        elif opcao == "5":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
        
        elif opcao == "0":
            print("Obrigado, volte sempre!")
            break

        else:
            print("Operação Invalida, selecione um dos numeros validos.")


def Depositar(saldo, extrato, valor):
    if valor > 0:
        saldo += valor
        extrato += f"Deposito: R$ {valor:.2f}\n"
        print("Deposito realizado com Sucesso!")
    else:
        print("O valor informado é invalido.")

    return saldo, extrato

def sacar(*, saldo, valor, numero_saques, MAX_SAQUES, limite, extrato):
    excedeu_saques = numero_saques >= MAX_SAQUES
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    
    if excedeu_saldo:
        print("Saldo insuficiente.")
    elif excedeu_saques:
        print("Valor ultrapassou o limite de saque diario.")
    elif excedeu_limite:
        print("Valor digitado excede o valor permitido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("Saque realizado com sucesso!")
    else:
        print("O valor informado é invalido.")

    return saldo, extrato, numero_saques

def Extrato(saldo, *, extrato):
    print("\n@@@@@@@-EXTRATO-@@@@@@@")
    print("Sem informações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")

def cad_usuario(usuarios):
    nome =  input("Informe o Nome de Usuario:")
    data_nascimento = input("Informe sua data de nascimento (dd/mm/aaaa):")
    endereco = input("Informe seu endereço (logradouro, n° - bairro - cidade/sigla estado):")
    cpf = input("Informe seu CPF (apenas números):")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("CPF já cadastrado no sistema!")
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("Usuário cadastrado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe seu CPF (apenas numeros)")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Conta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("Usuario não encontrado, saindo...")

main()
