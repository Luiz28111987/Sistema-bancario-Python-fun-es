import textwrap

def menu():
    # Variáveis do menu
    titulo = " MENU "
    global linha
    linha = "=" * 36
    mensagem_menu = """Escolha uma opção."""

    # Desenvolvendo o Menu
    menu_texto = f"""
{titulo.center(36, "=")}
{mensagem_menu}
[d]\tDepositar
[s]\tSacar
[e]\tExtrato
[nc]\tNova Conta
[lc]\tListar Contas
[nu]\tNovo Usuario
[lu]\tListar Usuarios
[q]\tSair
{linha}
    """
    return input(textwrap.dedent(menu_texto))
    
# RECEBER ARGUMENTOS SOMENTE POR POSIÇÃO
def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print(f"Deposito de {valor:.2f} Reais realizado com sucesso!")
    else:
        print("Digite um valor positivo.")
    return saldo, extrato

# RECEBER ARGUMENTOS SOMENTE POR NOMES
def sacar(*, saldo, valor, extrato, limite, numeros_saque, limite_saques):
    if valor <= 0:
        print("Digite um valor positivo.")
        return saldo, extrato, numeros_saque
    
    elif valor > limite:
        print("Valor maior que o limite de saque permitido.")
        return saldo, extrato, numeros_saque
    
    elif numeros_saque >= limite_saques:
        print("Quantidade de saques excedida")
        return saldo, extrato, numeros_saque
    
    elif valor > saldo:
        print("Saldo indisponível")
        return saldo, extrato, numeros_saque

    else:
        # Realiza o saque
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        print(f"Saque no valor de R$ {valor:.2f} realizado com sucesso!")
        numeros_saque += 1

        return saldo, extrato, numeros_saque

# RECEBER ARGUMENTOS POR POSIÇÃO E NOMES
def exibir_extrato(saldo, /, *, extrato, limite, numeros_saque, limite_saques):
    if not extrato:
        extrato_msg = "Não foram realizadas movimentações."
    else:
        extrato_msg = extrato

    linha = "=" * 36
    linha_2 = "-" * 36
    # Desenvolvendo o extrato
    imprimir_extrato = f"""
{linha}
Extrato Bancário
{linha}

Limites de saque: R$ {limite}
Saques permitidos: {limite_saques}
Saques utilizados: {numeros_saque}    

{linha_2}
Detalhes da Conta
{linha_2}
{extrato_msg}
{linha_2}
Saldo: R$ {saldo:.2f}
{linha_2}
{linha}
"""
    return imprimir_extrato

def criar_usuario(usuarios):
    cpf = input("Digite o CPF (somente números): ")
    # Remover pontuações do CPF
    cpf = ''.join(filter(str.isdigit, cpf))

    # Verificar se o CPF já existe na lista de usuários
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("CPF já cadastrado. Usuário não foi criado.")
        return
    
    nome = input("Digite o nome: ")
    data_nascimento = input("Digite a data de nascimento (dd/mm/aaaa): ")    
    endereco = input("Digite o endereço (logradouro, numero, bairro, cidade, sigla estado): ")    
    
    # Criar o dicionário do cliente
    cliente = {
        'nome': nome,
        'data_nascimento': data_nascimento,
        'cpf': cpf,
        'endereco': endereco,
        'contas': []  # Adiciona a lista de contas do usuário
    }
    
    # Adicionar o usuário à lista de usuários
    usuarios.append(cliente)
    print("Usuário criado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def listar_usuarios(usuarios):
    if not usuarios:
        print("Nenhum usuário cadastrado.")
    else:
        for usuario in usuarios:
            print(f"Nome: {usuario['nome']}, CPF: {usuario['cpf']}, Data de Nascimento: {usuario['data_nascimento']}, Endereço: {usuario['endereco']}")

def criar_conta(contas, agencia, usuarios, numero_conta):
    cpf = input("Digite o CPF do usuário para vincular a conta (somente números): ")
    # Remover pontuações do CPF
    cpf = ''.join(filter(str.isdigit, cpf))

    # Verificar se o CPF já existe na lista de usuários
    usuario = filtrar_usuario(cpf, usuarios)
    if not usuario:
        print("Usuário não encontrado. Conta não foi criada.")
        return
    
    # Criar o dicionário da conta
    conta = {
        'agencia': agencia,
        'numero_conta': numero_conta,
        'cpf': cpf,
        'saldo': 0,  # Inicializa o saldo da conta
        'extrato': ""  # Inicializa o extrato da conta
    }
    
    # Adicionar conta à lista de contas do usuário
    usuario['contas'].append(conta)
    contas.append(conta)
    print(f"Conta criada com sucesso! Número da conta: {conta['numero_conta']}")
    return numero_conta + 1  # Incrementa o número da conta

def listar_contas(contas):
    if not contas:
        print("Nenhuma conta cadastrada.")
    else:
        for conta in contas:
            print(f"Agência:\t{conta['agencia']} \nConta:\t\t{conta['numero_conta']} \nCPF:\t\t{conta['cpf']} \nSaldo:\t\tR$ {conta['saldo']:.2f}")

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    saldo = 0
    limite = 500
    extrato = ""
    numeros_saque = 0
    usuarios = []
    contas = []
    numero_conta = 1
    
    while True:

        opcao = menu()

        if opcao == "d":
            valor = float(input("Digite o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)            

        elif opcao == "s":
            valor = float(input("Digite o valor do saque: "))

            saldo, extrato, numeros_saque = sacar(
                saldo = saldo,
                valor = valor,
                extrato = extrato,
                limite = limite,
                numeros_saque = numeros_saque,
                limite_saques = LIMITE_SAQUES,
            )
            
        elif opcao == "e":
            extrato_str = exibir_extrato(
                saldo, 
                extrato=extrato,
                limite = limite,
                numeros_saque = numeros_saque,
                limite_saques = LIMITE_SAQUES,
            )
            print(extrato_str)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "lu":
            listar_usuarios(usuarios)

        elif opcao == "nc":
            numero_conta = criar_conta(
                contas, 
                agencia=AGENCIA,
                usuarios=usuarios,
                numero_conta=numero_conta
            )

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("Obrigado por usar nosso sistema!!!!")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()