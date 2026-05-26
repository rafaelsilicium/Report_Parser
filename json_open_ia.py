import litellm 
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

client_OpenIA = OpenAI(
    api_key=os.environ.get("AI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

response = client_OpenIA.chat.completions.create(
    model="gemini-3.5-flash",
    messages=[{"role": "user", 
               "content": "Você é um analista de futebol. Indique os melhores jogadores do S.C Internacional no elenco atual (maio de 2026), considerando 1 jogador por setor (goleiro, defensor, meio campo, atacante). Responda em formato json, organizando a resposta para criação de um arquivo .json a ser usado posteriormente. Headers do json: nome_jogador,posicao,idade,nacionalidade. Confira se os jogadores indicados realmente estão no time atual e se não foram transferidos para outros clubes (a exemplo do Vitão), com base nas últimas escalações para as partidas."}],
    response_format= {"type":"json_object"},
)

print(f"Resposta com bib OpenIA: {response.choices[0].message.content}")

try:
    #cria ou modifica um arquivo json contendo a resposta retornada da API 
    with open("open_ia_test.json", "w", encoding = "utf-8-sig") as json_file:
        json.dump(json.loads(response.choices[0].message.content),json_file,indent=4,ensure_ascii=False)
        
    print("\nArquivo JSON criado!")
    
except json.JSONDecodeError:
    print("Erro! Não foi possível criar o arquivo JSON!")
