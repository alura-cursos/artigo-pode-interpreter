from interpreter_utils import criar_arquivo, criar_assistente_dados_medicos, criar_thread, apagar_arquivo, apagar_thread, apagar_assistente
import os
from openai import OpenAI 
from dotenv import load_dotenv

load_dotenv()
cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def main():
    file_path = "transplantes_brasil.csv"
    arquivo = criar_arquivo(caminho_arquivo=file_path)
    assistente = criar_assistente_dados_medicos(file_id=arquivo.id)
    thread = criar_thread()

    pergunta = "Quais as características dos pacientes que pertencem aos 10% que mais recorrem a hemodialise?"

    message = cliente.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=pergunta
    )

    run = cliente.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistente.id
    )

    if run.status == "completed":
        mensagens_resposta = cliente.beta.threads.messages.list(
            thread_id=thread.id
        )

        for uma_mensagem in mensagens_resposta.data[0].content:
            if hasattr(uma_mensagem, "text") and uma_mensagem.text is not None:
                print("\n")
                print(uma_mensagem.text.value)
            elif hasattr(uma_mensagem, "image_file") and uma_mensagem.image_file is not None:
                resposta_da_openai = cliente.files.retrieve(uma_mensagem.image_file.file_id)
                image_data = cliente.files.content(resposta_da_openai.id)
                image_data_bytes = image_data.read()

                with open("grafico.png", "wb") as file:
                    file.write(image_data_bytes)
    else:
        print(run.status)

    apagar_arquivo(arquivo.id)
    apagar_thread(thread.id)
    apagar_assistente(assistente.id)

if __name__ == "__main__":
    main()
