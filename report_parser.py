"""
Report Parser V2
Autor: Rafael R. Schaeffer

Descrição:
Este script tem como objetivo ler arquivos de texto (.txt) contendo relatórios, extrair informações
específicas com base em headers pré-definidos, organizar esses dados extraídos e exportar
os resultados para um arquivo CSV (.csv).

Instruções de Uso:
1. Defina o caminho para o diretório onde os arquivos .txt estão localizados,
    bem como o caminho para o arquivo .csv onde os dados extraídos serão armazenados.
2. Atualize a lista de headers com os títulos específicos que você deseja extrair dos relatórios.
3. Execute o script. Ele lerá os arquivos .txt, verificará a presença dos
    headers, organizará os dados em um dicionário e exportará para o arquivo .csv.

Observações: O script inclui tratamento de erros para lidar com situações como arquivos ausentes,
erros de leitura/escrita e outros problemas inesperados que possam ocorrer durante a execução.
Certifique-se de que os arquivos .txt estejam formatados corretamente, com os headers
seguidos por um ":" e o conteúdo correspondente. Headers ausentes serão marcados
como "NÃO INFORMADO" no arquivo .csv resultante.

"""

from pathlib import Path
import csv


def verifica_headers_ausentes(
    conteudo_relatorio: list[str], headers: list[str]
) -> list[str]:
    """
    Verifica quais headers estão ausentes no conteúdo do relatório.

    Args:
        conteudo_relatorio (list[str]): Lista com linhas do conteúdo do relatório.
        headers (list[str]): Lista com os headers a serem verificados.

    Returns:
        list[str]: Lista com os headers ausentes.
    """
    headers_ausentes = []
    for header in headers:
        if not any(header.strip() in linha for linha in conteudo_relatorio):
            headers_ausentes.append(header.strip())

    return headers_ausentes


def organiza_conteudo_txt_em_dicionario(
    conteudo_relatorio: list[str], headers_ausentes: list[str]
) -> dict[str, str]:
    """
    Organiza o conteúdo do relatório em um dicionário, associando cada header
    a seu conteúdo correspondente.

    Args:
        conteudo_relatorio (list[str]): Lista contendo o conteúdo do relatório separado por linhas.
        headers_ausentes (list[str]): Lista com os headers ausentes no relatório.

    Returns:
        dict[str, str]: Dicionário com os headers como chaves e seus conteúdos como valores.

    """

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
