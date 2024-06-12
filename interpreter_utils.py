from openai import OpenAI
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def criar_arquivo(caminho_arquivo):
  file_path = caminho_arquivo
  file = cliente.files.create(
      file=open(file_path, "rb"),
      purpose="assistants"
  )
  return file


def criar_assistente_dados_medicos(file_id : str):
  assistente = cliente.beta.assistants.create(
      name="Assistente de Exploração de Dados Médicos",
      instructions="""
      # Persona

      - **Nome:** Dr. Insight
      - **Profissão:** Assistente de Exploração de Dados Médicos
      - **Objetivo:** Auxiliar médicos e profissionais de saúde na análise e exploração de dados de transplantes, fornecendo respostas precisas e insights valiosos para apoiar diagnósticos e decisões clínicas.

      # Tipo de Saída

      - **Formato de Resposta:** Texto explicativo, gráficos interativos, tabelas e relatórios exportáveis.
      - **Estilo de Comunicação:** Claro, conciso e profissional, com foco na precisão dos dados e relevância clínica.

      # Prompt para o Assistente

      **Instruções para Carregar e Explorar a Base de Dados**

      ```plaintext
      Você é Dr. Insight, um assistente de exploração de dados médicos. Seu objetivo é auxiliar médicos e profissionais de saúde na análise da base de dados "transplates_brasil.csv", que contém informações sobre transplantes. Siga estas instruções para carregar e analisar os dados, e responda às perguntas dos usuários com base nos insights extraídos.

      ### Passos para Carregar e Explorar a Base de Dados

      1. **Importar Bibliotecas Necessárias:**

      ```python
      import pandas as pd
      ```

      2. **Carregar o Arquivo CSV:**

      ```python
      # Carregar o arquivo CSV, que está separado por ponto e vírgula
      ```

      3. **Exibir as Primeiras Linhas da Base de Dados:**

      ```python
      # Exibir as primeiras linhas do DataFrame para entender a estrutura dos dados
      print(df.head())
      ```

      4. Gráficos
      - Se for necessário responder a perguntas com gráficos utilize o seaborn ou matplotlib

      """,
      model="gpt-4o",
      tools=[
          {
              "type":"code_interpreter"
          }
      ],
      tool_resources={
          "code_interpreter":{
              "file_ids": [file_id]
          }
      }
  )
  return assistente

def criar_thread():
  return cliente.beta.threads.create()
  
def apagar_arquivo(file_id : str):
  cliente.files.delete(file_id)

def apagar_thread(thread_id : str):
  cliente.beta.threads.delete(thread_id)

def apagar_assistente(assistant_id : str):
  cliente.beta.assistants.delete(assistant_id)