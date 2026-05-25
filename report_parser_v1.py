import os
from pathlib import Path
import csv

caminho_pasta_relatorios = "C:/Users/rafsc/OneDrive/Área de Trabalho/Relatorios txt"
caminho_arquivo_csv = (
    "C:/Users/rafsc/OneDrive/Área de Trabalho/Relatorios txt/projetos.csv"
)
headers = ["NOME DO PROJETO", "DATA", "STATUS", "RESUMO"]

Path_relatorios = Path(caminho_pasta_relatorios)


def atualiza_txt_incompleto(arquivo_relatorio, headers_ausentes):

    with open(arquivo_relatorio, "a", encoding="utf-8-sig") as editar_txt:
        for header in headers_ausentes:
            editar_txt.write(f"\n{header}: NÃO INFORMADO")


def strip_conteudo_resumo(conteudo_relatorio):
    return [linha.strip() for linha in conteudo_relatorio]


def verifica_headers_ausentes(conteudo_relatorio):

    headers_ausentes = []
    for header in headers:
        if not (
            any(
                header.strip() in linha
                for linha in strip_conteudo_resumo(conteudo_relatorio)
            )
        ):
            headers_ausentes.append(header)

    return headers_ausentes


def organiza_conteudo_txt_em_dicionario(conteudo_relatorio):

    conteudos_separados = {}
    for linha in conteudo_relatorio:
        if ":" in linha:
            header, conteudo = linha.split(":")
            conteudos_separados[header.strip()] = linha.strip(header).strip(": ")

    return conteudos_separados


def atualiza_leitura_relatorio(arquivo_relatorio):

    return arquivo_relatorio.read_text(encoding="utf-8-sig").splitlines()


def leitura_arquivos_txt():

    conteudos_agrupados = (
        []
    )  # Variável que receberá o conteúdo dos arquivos .txt unidos
    print("\nIniciando a leitura dos arquivos .txt\n")

    for arquivo_relatorio in Path_relatorios.glob("*.txt"):

        print(f"Analizando relatório {arquivo_relatorio}")

        conteudo_relatorio = atualiza_leitura_relatorio(arquivo_relatorio)

        if arquivo_relatorio.stat().st_size != 0:

            headers_ausentes = verifica_headers_ausentes(conteudo_relatorio)
            if len(headers_ausentes) != 0:
                #O código atualiza os relatorios txt incompletos, criando campos "NÃO INFORMADO" nas informações ausentes.]
                #Essa decisão foi tomada para facilitar a criação do csv, sendo o método que o dev conseguiu implementar na
                #versão do código. 
                atualiza_txt_incompleto(arquivo_relatorio, headers_ausentes)
                conteudo_relatorio = atualiza_leitura_relatorio(arquivo_relatorio)

            conteudos_agrupados.append(
                organiza_conteudo_txt_em_dicionario(conteudo_relatorio)
            )

    return conteudos_agrupados  # Retorna a variável com todos os conteúdos unidos


def insere_headers_csv(planilha_csv):
    dicionar_headers = csv.writer(planilha_csv, delimiter=";")
    dicionar_headers.writerow(headers)
    print("Cabeçalho do arquivo .csv adicionado!")


def cria_arquivo_csv():

    with open(
        caminho_arquivo_csv, "a", newline="", encoding="utf-8-sig"
    ) as planilha_csv:

        if os.path.getsize(caminho_arquivo_csv) == 0:
            insere_headers_csv(planilha_csv)

        editar_csv = csv.DictWriter(planilha_csv, fieldnames=headers, delimiter=";")
        editar_csv.writerows(leitura_arquivos_txt())
        planilha_csv.close()
        print("\nEdição do arquivo .csv finalizada!")


def main():

    print("\n--------Report Parser V1--------\n")
    cria_arquivo_csv()

    print("Fim da execução...")


if __name__ == "__main__":
    main()
