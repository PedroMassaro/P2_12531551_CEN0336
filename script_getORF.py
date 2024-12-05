#!/usr/bin/env python3

import sys

#Dicionária para tradução dos ORF
tabela_de_traducao = {
    'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
    'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R', 'AGA': 'R', 'AGG': 'R',
    'AAT': 'N', 'AAC': 'N',
    'GAT': 'D', 'GAC': 'D',
    'TGT': 'C', 'TGC': 'C',
    'CAA': 'Q', 'CAG': 'Q',
    'GAA': 'E', 'GAG': 'E',
    'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G',
    'CAT': 'H', 'CAC': 'H',
    'ATT': 'I', 'ATC': 'I', 'ATA': 'I',
    'TTA': 'L', 'TTG': 'L', 'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',
    'AAA': 'K', 'AAG': 'K',
    'ATG': 'M',
    'TTT': 'F', 'TTC': 'F',
    'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
    'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S', 'AGT': 'S', 'AGC': 'S',
    'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
    'TGG': 'W',
    'TAT': 'Y', 'TAC': 'Y',
    'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V',
    'TAA': '*', 'TGA': '*', 'TAG': '*'
}

#Função para ler o arquivo fasta - a
def ler_fasta(caminho):
    print(f"Lendo o arquivo {caminho} e armazenando em uma lista de tuplas (cabeçalho, sequência).")
    try:
        #Com 'with' para a sequência ser fechada posteriormente.
        with open(caminho, "r") as arquivo:
            registros = []
            header = None
            sequencia = []
            for linha in arquivo:
                #Retira os espaços entre as linhas (\n)
                linha = linha.strip()
                if linha.startswith(">"):
                    #Concatena as sequências após já ter lido todas as linhas
                    if header:
                        registros.append((header, "".join(sequencia)))
                    #Reinicia o processo para a próxima sequência
                    header = linha[1:]
                    sequencia = []
                else:
                    sequencia.append(linha)
            #Armazena a última sequência
            if header:
                registros.append((header, "".join(sequencia)))
            return registros

    #Controle de entrada de arquivo
    except FileNotFoundError:
        print(f"Erro: Arquivo {caminho} não encontrado.")
        sys.exit(1)

#Buscando os ORF mais compridos que inicia em  um codon de início da tradução e termina com um códon de terminação da tradução
def encontrar_orf(sequencia):
    stop_codons = {"TAA", "TAG", "TGA"}
    start_codon = "ATG"
    #Dicionário para armazena informação da sequência
    max_orf = {"seq": "", "frame": 0, "start": 0, "end": 0}
    comp = len(sequencia)

    #Realizando as três fases de leitura. Com 'frame' sendo 1,2 e 3; e +1 a sequência original e -1 a sequência complementar (Com a inversão e transtrição
    for frame in range(3):
        for sentido, seq in [(+1, sequencia), (-1, sequencia[::-1].translate(str.maketrans("ATCG", "TAGC")))]:
            #Definindo o frame de leitura
            offset = frame if sentido == 1 else -(frame + 1)
            #Retirando os nucleotídeos fora do frame
            seq_to_check = seq[frame:]
            #Buscando codon de início
            for i in range(0, len(seq_to_check) - 2, 3):
                codon = seq_to_check[i:i+3]
                if codon == start_codon:
                    #Buscando codon de parada
                    for j in range(i, len(seq_to_check) - 2, 3):
                        codon_j = seq_to_check[j:j+3]
                        if codon_j in stop_codons:
                            orf_length = j - i + 3
                            #Se o ORF for maior do que algum que já está salvo, esse ORF será salvo no dicionário
                            if orf_length > len(max_orf["seq"]):
                                #Ajustando a fase de leitura
                                mapa_offset = {0: 1, 1: 2, 2: 3, -1: 4, -2: 5, -3: 6}
                                fase = mapa_offset[offset]
                                max_orf = {
                                    "seq": seq_to_check[i:j+3],
                                    "frame": fase,
                                    "start": i + 1 if sentido == 1 else comp - j,
                                    "end": j + 3 if sentido == 1 else comp - i,
                                }
                            break
    return max_orf

#Traduzindo o ORF mais comprido de cada sequência usando a tabela de tradução
def traduzir_orf(orf_seq):
    aminoacidos = []
    for i in range(0, len(orf_seq) - 2, 3):
        codon = orf_seq[i:i+3]
        aminoacidos.append(tabela_de_traducao.get(codon, 'X'))  #'X' para códons inválidos
    return "".join(aminoacidos).split('*')[0]  #Parar na primeira parada (*)

#Salvando as saídas desejadas em arquivos
def escrever_fasta(registros, caminho):
    try:
        with open(caminho, "w") as arquivo:
            for header, sequencia in registros:
                arquivo.write(f">{header}\n{sequencia}\n")
    except Exception as e:
        print(f"Erro ao salvar arquivo fasta: {e}")
        sys.exit(1)

def main():
    """Função principal para executar o script."""
    #Controle para entrada de apenas um arquivo fasta
    if len(sys.argv) != 2:
        print("Uso: python script_getORF.py <arquivo_multifasta>")
        sys.exit(1)

    arquivo_fasta = sys.argv[1]

    #Leitura do arquivo e separação entre o nome e a sequência
    registros = ler_fasta(arquivo_fasta)
    saida_dna = []
    saida_proteina = []

    print("Iniciando processamento das sequências. Identificando os ORFs e traduzindo o com maior extensão de cada seqência.")
    #Com a sequência lida, iniciando o processo de encontrar o ORF mais comprido e traduzi-lo
    for header, sequencia in registros:
        #Buscando os ORF mais comprido para cada sequência
        orf = encontrar_orf(sequencia)
        #Traduzindo o ORF mais cromprido
        peptide = traduzir_orf(orf["seq"])
        #Renomeando o cabeçalho
        novo_header = f"{header}_frame{orf['frame']}_START{orf['start']}_END{orf['end']}"
        #Saídas
        saida_dna.append((novo_header, orf["seq"]))
        saida_proteina.append((novo_header, peptide))

    #Salvando nos respectivos arquivos o ORF mais comprido e sua tradução
    escrever_fasta(saida_dna, "ORF.fna")
    escrever_fasta(saida_proteina, "ORF.faa")
    print("Processamento concluído. Arquivos ORF.fna e ORF.faa gerados e disponibilizados em seu diretório.")

if __name__ == "__main__":
    main()
