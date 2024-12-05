#!/usr/bin/env python3

class errorINTERVALO(Exception):
    pass

# Inicializando variáveis
total = 0
contador_notas = 0

print("Insira 10 notas, de 1 a 10, para calcular a média da disciplina:")

# Loop para coletar 10 notas
while contador_notas < 10:
   try:

     nota = float(input(f"Digite a nota {contador_notas + 1}: "))

     #Verificando se a entrada é válida
     if nota < 0 or nota > 10:
        raise errorINTERVALO("Erro: A nota deve estar entre 0 e 10.")

     #Soma a nota ao total e incrementa o contador
     total += nota
     contador_notas += 1

   #Captura o erro na conversão para float
   except ValueError:
     print("Erro: A nota deve ser um número de ponto flutuante.")
   #Se uma entrada está dentro do intervalo desejado
   except errorINTERVALO:
     print("Erro: A nota deve estar entre 0 e 10.")

# Calcula a média
media = total / 10

# Exibe a média
print(f"\nA média da disciplina é: {media:.2f}")

