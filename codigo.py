#Fase 1 projeto integrador
#MENU
import sys
import time
import pandas as pd
import oracledb
import numpy as np

#conexão com o oracle
conexao = oracledb.connect(
    user="sys",
    password="h135150@",
    dsn="localhost/XEPDB1",
    mode = oracledb.SYSDBA)
cursor = conexao.cursor()


### Começo Loading Bar
def loading_bar():
    toolbar_width = 10
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+1))

    for i in range(toolbar_width):
        time.sleep(0.10)  # Simulando algum processo que está sendo executado
        sys.stdout.write(".")
        sys.stdout.flush()

    sys.stdout.write("\n")
#Fim Loading Bar

#definindo função da tabela do bd

def data_bank ():
    cursor.execute("SELECT CÓDIGO_PRODUTO, NOME, DESCRICAO, CP, CF, CV, IV, ML FROM CADASTRO_PRODUTO")
    linhas = cursor.fetchall()

    # Exibir os dados com a coluna descriptografada
    for linha in linhas:
        CÓDIGO_PRODUTO, NOME, DESCRICAO, CP, CF, CV, IV, ML = linha
        info_descriptografada = descripto(DESCRICAO)
        print(f"ID: {CÓDIGO_PRODUTO}, Nome: {NOME}, Descricao: {info_descriptografada}, CP: {CP}, CF: {CF}, CV: {CV}, IV: {IV}, ML: {ML}")

#Definindo a criptografia

alfabeto = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19, 'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 0}

def criptografando(desc):
    pal = desc.upper()
    matriz_pal = np.array([[],[]])
    main_matriz = np.array([[4,3],[1,2]])
    

    if len(pal) %2 !=0:
        pal+='A'
        

    matriz_pal = pal_em_matriz(pal)
    pal = pal[:-1]
    pal_cripto = np.dot(main_matriz, matriz_pal) % 26
    palavra_cripto = formando_palavra(pal_cripto)
    return palavra_cripto
    

def descripto(a):
  pal_cripto = a.upper()
  matriz_pal_num= pal_em_matriz(pal_cripto)
  
  determinante= 4*2-3*1
  chave_m_i = np.array([[2,-3],[-1,4]])

  det_inversas = {1: 1, 3: 9, 5: 21, 7: 15, 9: 3, 11: 19, 15: 7, 17: 23, 19: 11, 21: 5, 23: 17, 25: 25}
  for chave, valor in det_inversas.items():
      if determinante == chave:
          determinante = valor
          break
  chave_m_i *= determinante
  matriz_pal_num = np.dot(chave_m_i, matriz_pal_num)
  palavra_descripto = formando_palavra(matriz_pal_num)
  return palavra_descripto
  




def pal_em_matriz(pal):
        letras = []
        matriz_pal_num = np.array([[], []])
        pal=pal.replace(" ", "")
        for letra in range(len(pal)):
            for chave, valor in alfabeto.items():
                if pal[letra] == chave:
                    letras.append(valor)
        for i in range(0, len(pal)-1, 2):  
            novaColuna = np.array([[letras[i]], [letras[i+1]]])
            matriz_pal_num = np.append(matriz_pal_num, novaColuna, axis=1)
        return matriz_pal_num



def formando_palavra(matriz_pal_num):
    palavra = ''
    for i in range(matriz_pal_num.shape[1]):
        for j in range(matriz_pal_num.shape[0]):
            valor = matriz_pal_num[j, i] % 26
            for chave, val in alfabeto.items():
                if val == valor:
                    palavra += chave
    return palavra



#Começo do programa
print(f"<--------------------CADASTRO DE PRODUTO-------------------->")
x = int(input('[1] Para cadastrar um novo produto: \n[2] Para alterar um produto: \n[3] Para apagar um produto: \n[4] Listar os produtos já cadastrados: \n[5] Sair:  '))
print("-"*61)     
if (x == 1):
    cod=int(input("\nDigite o código do produto: ")) 
    loading_bar()
    print("\nRegistrado com sucesso!")

    prod=str(input("\nDigite o nome do produto: "))
    loading_bar()
    print("\nRegistrado com sucesso!")

    desc=input("\nDigite a descrição do produto: ")
    loading_bar()
    print("\nRegistrado com sucesso!")

    CP=float(input("\nDigite o custo do produto em reais: "))
    loading_bar()
    print("\nRegistrado com sucesso!")

    CF=float(input("\nDigite o custo fixo em %: "))
    loading_bar()
    print("\nRegistrado com sucesso!")

    CV=float(input("\nDigite a comissão de venda em %: "))
    loading_bar()
    print("\nRegistrado com sucesso!")

    IV=float(input("\nDigite o valor dos impostos em %: "))
    loading_bar()
    print("\nRegistrado com sucesso!")

    ML=float(input("\nDigite o valor da rentabilidade em %: "))
    loading_bar()
    print("\nRegistrado com sucesso!")


    PV=0
    PV=CP/(1-((CF+CV+IV+ML)/(100)))
    CA=(CP*100)/PV
    RB=PV-CP
    RBB=(RB*100)/PV
    CFF=(PV/100)*CF
    CVV=(PV/100)*CV
    IVV=(PV/100)*IV
    OC=((CFF)+(CVV)+(IVV))
    OCC=((CF)+(CV)+(IV))
    ML=((RBB)-(OCC))
    MLL=((RB)-(OC))



    #Criando a tabela
    df=pd.DataFrame({"Descrição":["Preco de venda","Custo de aquisicao(fornecedor)",
    "Receita bruta (A-B)","Custo fixo/Administrativo","Comissao de vendas","Impostos","Outros custos (D + E + F)",
    "Rentabilidade", ],
                    "Valor":[PV,CP,RB,CFF,CVV,IVV,OC,MLL],
                    "%":["100%",CA,RBB,CF,CV,IV,OCC,ML]})

    print(df)

    #Definindo Rentabilidade
    if ML > 20 and ML < 100:
        print("\nO produto se encontra na faixa de lucro ALTO.")
    elif ML > 10 and ML < 20:
        print("\nO produto se encontra na faixa de lucro MÉDIO.")
    elif ML > 0 and ML < 10:
        print("\nO produto se encontra na faixa de lucro BAIXO.")
    elif ML == 0:
        print("\nO produto se encontra em EQUILÍBRIO.")
    elif ML < 0:
        print("\nO produto se encontra em PREJUÍZO.")
    elif ML > 100:
        print("\nErro.")

#Confirmando o resgistro do novo produto

    y = int(input("Para registrar esse produto em definitivo digite [1]. Caso contrário, digite [2]: "))
    loading_bar()
    if (y == 1):
        palavra_cripto = criptografando(desc)
        
        cursor.execute (f"INSERT INTO CADASTRO_PRODUTO (Código_produto,Nome,Descricao,cp,cf,cv,iv,ml) VALUES ({cod},'{prod}','{palavra_cripto}',{CP},{CF},{CV},{IV},{ML})")
        conexao.commit()
        print(f"\n\tO produto foi registrado!")
        loading_bar()
        data_bank()
            

    elif (y == 2):
        print(f"\n\tNenhum produto foi registrado.")


#Alterar produto

elif (x == 2):
    loading_bar()
    data_bank()
    loading_bar()
    print(f"<----------------------------------------------------------->")
    z = int(input("[1] Para alterar o código: \n[2] Para alterar o nome: \n[3] Para alterar a descrição: \n[4] Para alterar o preço: \n[5] Para alterar o custo fixo: \n[6] Para alterar comissão de vendas: \n[7] Para alterar os impostos: \n[8] Para alterar a rentabilidade: "))
    print(f"<----------------------------------------------------------->")
    if (z == 1):
        loading_bar()
        y = int(input("Digite o código do produto que se quer alterar: "))
        loading_bar()
        cod = int(input("Digite o novo código do produto: "))
        cursor.execute (f"UPDATE CADASTRO_PRODUTO SET Código_produto = {cod} WHERE Código_Produto = {y}")
        conexao.commit()
        loading_bar()
        data_bank()
    elif(z == 2):
        loading_bar()
        y = int(input("Digite o código do produto que se quer alterar: "))
        loading_bar()
        prod = str(input("Digite o novo nome do produto: "))
        cursor.execute (f"UPDATE CADASTRO_PRODUTO SET Nome = '{prod}' WHERE Código_Produto = {y}")
        conexao.commit()
        loading_bar()
        data_bank()
    elif(z == 3):
        loading_bar()
        y = int(input("Digite o código do produto que se quer alterar: "))
        loading_bar()
        desc = str(input("Digite a nova descrição do produto: "))
        palavra_cripto = criptografando(desc)
        cursor.execute (f"UPDATE CADASTRO_PRODUTO SET Descricao = '{palavra_cripto}' WHERE Código_Produto = {y}")
        conexao.commit()
        loading_bar()
        data_bank()
    elif(z == 4):
        loading_bar()
        y = int(input("Digite o código do produto que se quer alterar: "))
        loading_bar()
        CP=float(input("Digite o novo custo do produto em reais: ")) 
        cursor.execute (f"UPDATE CADASTRO_PRODUTO SET cp = {CP} WHERE Código_Produto = {y}")
        conexao.commit()
        loading_bar()
        data_bank()
    elif(z == 5):
        loading_bar()
        y = int(input("Digite o código do produto que se quer alterar: "))
        loading_bar()
        CF=float(input("\nDigite o novo custo fixo em %: "))
        cursor.execute (f"UPDATE CADASTRO_PRODUTO SET cf = {CF} WHERE Código_Produto = {y}")
        conexao.commit()
        loading_bar()
        data_bank()
    elif(z == 6):
        loading_bar()
        y = int(input("Digite o código do produto que se quer alterar: "))
        loading_bar()
        CV=float(input("Digite a nova comissão de venda em %: "))
        cursor.execute (f"UPDATE CADASTRO_PRODUTO SET cf = {CV} WHERE Código_Produto = {y}")
        conexao.commit()
        loading_bar()
        data_bank()
    elif(z == 7):
        loading_bar()
        y = int(input("Digite o código do produto que se quer alterar: "))
        loading_bar()
        IV=float(input("Digite o novo valor dos impostos em %: "))
        cursor.execute (f"UPDATE CADASTRO_PRODUTO SET cf = {IV} WHERE Código_Produto = {y}")
        conexao.commit()
        loading_bar()
        data_bank()
    elif(z == 8):
        loading_bar()
        y = int(input("Digite o código do produto que se quer alterar: "))
        loading_bar()
        ML=float(input("Digite o novo valor da rentabilidade em %: "))
        cursor.execute (f"UPDATE CADASTRO_PRODUTO SET cf = {ML} WHERE Código_Produto = {y}")
        conexao.commit()
        loading_bar()
        data_bank()


#Deletar um produto

elif(x == 3):
    print(f"<----------------------------------------------------------->")
    data_bank()
    print(f"<----------------------------------------------------------->")
    cod=int(input("\nDigite o código do produto que se deseja deletar: ")) 
    pergunta = int(input(f"TEM CERTEZA QUE DESEJA APAGAR O PRODUTO DE CÓDIGO {cod}? SIM: [1] \nNÃO [2]: "))
    if(pergunta == 1):
        cursor.execute (f"DELETE FROM CADASTRO_PRODUTO WHERE Código_produto = {cod}")
        conexao.commit()
        loading_bar()
        data_bank()
    elif(pergunta == 2):
        sys.exit()

    
#Produtos já cadastrados

elif (x == 4):
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM CADASTRO_PRODUTO")
    var = cursor.fetchall()
    conexao.commit()

    for i in var :
            cod, prod, desc, CP, CF, CV, IV, ML = i
            
            desc = descripto(desc)

            PV=0
            PV=CP/(1-((CF+CV+IV+ML)/(100)))
            CA=(CP*100)/PV
            RB=PV-CP
            RBB=(RB*100)/PV
            CFF=(PV/100)*CF
            CVV=(PV/100)*CV
            IVV=(PV/100)*IV
            OC=((CFF)+(CVV)+(IVV))
            OCC=((CF)+(CV)+(IV))
            ML=((RBB)-(OCC))
            MLL=((RB)-(OC))



            #Criando a tabela
            df=pd.DataFrame({"Descrição":["Preco de venda","Custo de aquisicao(fornecedor)",
            "Receita bruta (A-B)","Custo fixo/Administrativo","Comissao de vendas","Impostos","Outros custos (D + E + F)",
            "Rentabilidade", ],
                            "Valor":[PV,CP,RB,CFF,CVV,IVV,OC,MLL],
                            "%":["100%",CA,RBB,CF,CV,IV,OCC,ML]})
            
            print(f"<----------------------------------------------------------->")
            print(f"\n{cod}             {prod}                {desc}\n\t{df}")

            #Definindo Rentabilidade
            if ML > 20 and ML < 100:
                print("\nO produto se encontra na faixa de lucro ALTO.")
            elif ML > 10 and ML < 20:
                print("\nO produto se encontra na faixa de lucro MÉDIO.")
            elif ML > 0 and ML < 10:
                print("\nO produto se encontra na faixa de lucro BAIXO.")
            elif ML == 0:
                print("\nO produto se encontra em EQUILÍBRIO.")
            elif ML < 0:
                print("\nO produto se encontra em PREJUÍZO.")
            elif ML > 100:
                print("\nErro.")

    print(f"<----------------------------------------------------------->")


#Sair do programa

elif(x == 5):
    sys.exit()
