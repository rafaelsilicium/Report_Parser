# Report Parser 
[![Versão do Python](https://img.shields.io/badge/Python-3.11--3.14-blue)](https://python.org)

O projeto  **Report Parser** tem como objetivo o preenchimento de arquivo .csv seguindo estrutura especificada a partir de relatórios parciais em formato .txt, consolidando e agrupando as diferentes etapas dos projetos em um único relatório geral.

[Linguagem]: Python 3.14

## Funcionalidades
- **Leitura de resumo de relatórios .txt:** O _Parser_ faz a leitura e interpretação de todos os relatórios .txt do diretório indicado;
- **Criação de arquivo .csv unificada:** Realiza o preenchimento de um arquivo .csv com os dados dos projetos, indexando as colunas a partir do cabeçalho padronizado

## Bibliotecas Utilizadas
A versão atual do Report Parser utiliza apenas bibliotecas nativas Python (Pathlib e csv), não necessitando instalar adicionais

## Padrão dos arquivos de relatórios .txt
Para utilização no _Parser_, os relatórios dos projetos devem seguir um padrão estipulado, contendo o padrão **CABEÇALHO: CONTEÚDO**, conforme o exemplo abaixo:

Exemplo de *cabeçalhos:* ["NOME DO PROJETO", "DATA", "STATUS", "RESUMO"]

Exemplo de arquivo .txt:

    NOME DO PROJETO: Projeto de Teste
    
    DATA: 27/05/2026
    
    STATUS: Em Desenvolvimento
    
    RESUMO: Este texto tem como objetivo representar um resumo de um projeto em desenvolvimento, exemplificando um modelo compatível com o Report Parser.

O arquivo .csv gerado para este exemplo será:


| NOME DO PROJETO | DATA | STATUS | RESUMO |
| :--- | :--- | :--- | :--- |
| Projeto de Teste | 27/05/2026 | Em Desenvolvimento | Este texto tem como objetivo representar um resumo de um projeto em desenvolvimento, exemplificando um modelo compatível com o Report Parser. |



**ATENÇÃO!** Caso um arquivo de relatório esteja incompleto, o _Parser_ irá adicionar a mensagem "NÃO INFORMADO" no arquivo .csv ao campo ausente. Arquivos vazios serão ignorados. 

## Edições necessárias
Para utilizar o _Parser_ deve-se editar os caminhos do arquivo .csv, a pasta de relatórios .txt e a lista de cabeçalhos existente na função main(), conforme exemplo abaixo:

``` python

path_arquivo_csv = Path("caminho_pasta_arquivo_CSV_aqui/nome_do_arquivo_csv.csv")
path_relatorios = Path("caminho_pasta_relatorios_txt_aqui")
headers = ["HEADER_1", "HEADER_2", "HEADER_3", "HEADER_4"]

```

## Outros projetos do repositório
O repositório está sendo utilizado para armazenamento de outros scripts teste, como o **llm_extractor.py**. O projeto em questão está em desenvolvimento, ainda sem refatoração e versão final. 

