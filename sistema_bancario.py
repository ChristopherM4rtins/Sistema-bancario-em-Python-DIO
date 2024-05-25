menu = """

[1] Sacar
[2] Depositar
[3] Extrato
[0] Sair

=>"""

limite = 500
saldo = 0
MAX_SAQUES = 3
Extrato = ""
numero_saques = 0


while True:
    opcao = input(menu)

    if opcao == "2":
        print("Depositar")
        valor = int(input("Informe o Valor de Deposito:"))

        if valor > 0:
            saldo += valor
            Extrato += f"Deposito: R$ {valor:.2f}\n"
            print("Deposito realizado com Sucesso!")
        else:
            print("O valor informado é invalido.")


    elif opcao == "1":
        print("Sacar")
        valor = int(input("Informe o Valor de Saque:"))

        excedeu_saques = numero_saques >= MAX_SAQUES
        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
    
        if excedeu_saldo:
            print("Saldo insuficiente.")
        elif excedeu_saques:
            print("Valor ultrapassou o limite de saque diario.")
        elif excedeu_limite:
            print("Limite excede o valor permitido.")

        elif valor > 0:
            saldo -= valor
            Extrato += f"Saque: RS {valor:.2f}\n"
            numero_saques += 1
            print("Saque realizado com sucesso!")
        else:
            print("O valor informado é invalido.")
      

    elif opcao == "3":
        print("\n@@@@@@@-EXTRATO-@@@@@@@")
        print("Sem informações." if not Extrato else Extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")

    elif opcao == "0":
        print("Obrigado, volte sempre!")
        break

    else:
        print("Operação Invalida, selecione um dos numeros validos.")


    