#!/usr/bin/env python3

import sys

#Função recursiva para fazer a contagem do número de nós e folhas
def contar_nos(arvore):
    """
    Essa função irá calcular o número total de nós e folhas em uma árvore representada por um dicionário de dicionários.
    Parâmetros:
        arquivo.txt: Representação da árvore por um dic. de dic. (ex. arvore.txt).
    Retorna:
        int: O número total de nós e folhas na árvore.
    """
    try:
        #Verifica se a entrada é um dicionário
        if not isinstance(arvore, dict):
            raise ValueError("A árvore deve ser representada como um dicionário de dicionários.")

        #Conta o nó raiz, por isso inicia em 1
        total_nos = 1

        #Para cada chave da árvore (subárvore), a função será novamente chamada para contagem dos nós e folhas
        for chave in arvore:
           subarvore = arvore[chave]
           #Se a subárvore for um dicionário, chama recursivamente a função contar_nos
           if isinstance(subarvore, dict):
              total_nos += contar_nos(subarvore)  #Contagem
           #Caso não apresente um subárvore, seja uma folha, adiciona +1 - sem chamar a função novamente
           else:
              total_nos += 1

        return total_nos

    except Exception as e:
        print(f"Erro ao processar a árvore: {e}")
        return 0


#Verifica se houve a inserção de apenas um argumento na linha de comando
if len(sys.argv) != 2:
    print("Uso: python arvore_filo.py <caminho_do_arquivo>")
else:
    try:

        caminho_arquivo = sys.argv[1]
        #Leitura do arquivo e converte para um dicionário
        with open(caminho_arquivo, "r") as arquivo:
            conteudo = arquivo.read()
        arvore = eval(conteudo)

        #Chama a função e exibe o resultado
        total_nos = contar_nos(arvore)
        print(f"Número total de nós e folhas na árvore: {total_nos}")
    except FileNotFoundError:
        print("Erro: O arquivo inserido não foi encontrado.")
    except SyntaxError:
        print("Erro: O arquivo contém um formato inválido.")
    except Exception as e:
        print(f"Erro inesperado: {e}")
