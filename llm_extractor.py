import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pathlib import Path
import json

load_dotenv() #Carrega variáveis de ambiente

client_gemini = genai.Client(api_key = os.environ.get("AI_API_KEY")) #inicia client gemini com a key configurada no arquivo .env
caminho_pasta = Path("C:/Users/rafsc/OneDrive/Área de Trabalho/Report Parser V1/Relatorios txt") #Indicação da pasta dos arquivos resumo 
nome_arquivo_txt_prompt = "gemini_prompt.txt" #nome do arquivo contendo o prompt 
encoding_ = "utf-8-sig" #tipo de decodificação
conteudo_todos_resumos = [] #variável para juntar os conteudos dos resumos

prompt_config = types.GenerateContentConfig(
        response_mime_type="application/json" #Configura a resposta da API Gemini sempre em formato json
)

with open(nome_arquivo_txt_prompt, 'r', encoding = encoding_) as prompt_txt:
    print("Lendo conteudo do prompt...\n")
    api_gemini_prompt = prompt_txt.read() #Lê o conteúdo do arquivo .txt contendo o prompt para da aplicação
    
print("Lendo arquivos de resumo: \n")
for arquivo_resumo in caminho_pasta.glob('*.txt'): #Lê todos os arquivos .txt existentes na pasta
        
        conteudo_resumo = arquivo_resumo.read_text(encoding = encoding_).splitlines()
        print (f"\nLendo o arquivo {arquivo_resumo.name}")
        
        if arquivo_resumo.stat().st_size != 0: #Adiciona à "conteudo_todos_resumos" o conteúdo do arquivo .txt de resumo
                                                #caso este não seja vazio
            conteudo_todos_resumos.append(conteudo_resumo)

#Faz a chamada da API considerando a mensagem do prompt e o conteúdo de todos os resumos unidos
print("Solicitando resposta ao API Gemini...")
gemini_reply =client_gemini.models.generate_content(
        model = 'gemini-2.5-flash', #configura o modelo a ser utilizado
        contents = api_gemini_prompt + ' '.join(map(str, conteudo_todos_resumos)),
        config = prompt_config #adiciona a configuração de resposta em json
)

#apresenta o texto da resposta recebida
print("Resposta Gemini API:\n" )
print(gemini_reply.text)

try:
    #cria ou modifica um arquivo json contendo a resposta retornada da API 
    with open("llm_extractor.json", "w", encoding = encoding_) as json_file:
        json.dump(json.loads(gemini_reply.text),json_file,indent=4,ensure_ascii=False)
        
    print("\nArquivo JSON criado!")
    
except json.JSONDecodeError:
    print("Erro! Não foi possível criar o arquivo JSON!")
