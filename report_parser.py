from pathlib import Path
import csv


def verifica_headers_ausentes(conteudo_relatorio, headers):

    headers_ausentes = []
    for header in headers:
        if not (any(header.strip() in linha for linha in conteudo_relatorio)):
            headers_ausentes.append(header.strip())

    return headers_ausentes


def organiza_conteudo_txt_em_dicionario(conteudo_relatorio, headers_ausentes):

    conteudos_separados = {}
    for linha in conteudo_relatorio:
        if ":" in linha:
            header, conteudo = linha.split(":", 1)
            conteudos_separados[header.strip()] = conteudo.strip()

    if len(headers_ausentes) != 0:
        for header in headers_ausentes:
            conteudos_separados[header.strip()] = "NÃO INFORMADO"

    return conteudos_separados


def leitura_relatorio(arquivo_relatorio):

    return arquivo_relatorio.read_text(encoding="utf-8-sig").splitlines()


def leitura_arquivos_txt(path_relatorios, headers):

    conteudos_agrupados = []
    print("\nIniciando a leitura dos arquivos .txt\n")

    for arquivo_relatorio in path_relatorios.glob("*.txt"):
        try:
            print(f"Analisando relatório {arquivo_relatorio}")

            conteudo_relatorio = leitura_relatorio(arquivo_relatorio)

            if arquivo_relatorio.stat().st_size != 0:

                headers_ausentes = verifica_headers_ausentes(
                    conteudo_relatorio, headers
                )
                conteudos_agrupados.append(
                    organiza_conteudo_txt_em_dicionario(
                        conteudo_relatorio, headers_ausentes
                    )
                )

        except Exception as erro:
            print(f"Erro! Um erro inesperado aconteceu! Erro: {erro}")

    return conteudos_agrupados


def insere_headers_csv(planilha_csv, headers):
    dicionar_headers = csv.writer(planilha_csv, delimiter=";")
    dicionar_headers.writerow(headers)
    print("\nCabeçalho do arquivo .csv adicionado!")


def cria_arquivo_csv(path_arquivo_csv, dados_parser, headers):

    try:
        with open(
            path_arquivo_csv, "a", newline="", encoding="utf-8-sig"
        ) as planilha_csv:

            if path_arquivo_csv.stat().st_size == 0:
                insere_headers_csv(planilha_csv, headers)

            editar_csv = csv.DictWriter(planilha_csv, fieldnames=headers, delimiter=";")
            editar_csv.writerows(dados_parser)
            print("\nEdição do arquivo .csv finalizada!")

    except FileNotFoundError:
        print("Erro! O arquivo .csv indicado não existe!")

    except Exception as erro:
        print(
            f"\nErro! Não foi possível abrir o arquivo .csv! \nA edição não foi realizada! Erro: {erro}"
        )


def main():

    path_arquivo_csv = Path(
        "C:/Users/rafsc/OneDrive/Área de Trabalho/Relatorios txt/projetos.csv"
    )
    path_relatorios = Path("C:/Users/rafsc/OneDrive/Área de Trabalho/Relatorios txt")
    headers = ["NOME DO PROJETO", "DATA", "STATUS", "RESUMO"]

    print("\n--------Report Parser V2--------\n")

    if path_relatorios.exists() and path_relatorios.is_dir():

        dados_parser = leitura_arquivos_txt(path_relatorios, headers)

        if len(dados_parser) != 0:
            cria_arquivo_csv(path_arquivo_csv, dados_parser, headers)

        else:
            print(
                "Atenção! A leitura dos relatórios retornou nenhum dado. Execução não realizada."
            )

    else:
        print("Erro! O diretório indicado para os relatórios não existe!")

    print("\nFim da execução...")


if __name__ == "__main__":
    main()
