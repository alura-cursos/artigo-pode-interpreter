from interpreter_utils import criar_arquivo, criar_assistente_dados_medicos, criar_thread, apagar_arquivo, apagar_thread, apagar_assistente

def main():
    file_path = "transplates_brasil.csv"
    arquivo = criar_arquivo(file_path)
    assistente = criar_assistente_dados_medicos(file_id=arquivo["id"])
    thread = criar_thread()

    pergunta = "Quais as características dos pacientes que pertencem aos 10% que mais recorrem a hemodialise?"

    message = openai.Thread.message_create(
        thread_id=thread["id"],
        role="user",
        content=pergunta
    )

    run = openai.Thread.run_create_and_poll(
        thread_id=thread["id"],
        assistant_id=assistente["id"]
    )

    if run["status"] == "completed":
        mensagens_resposta = openai.Thread.message_list(
            thread_id=thread["id"]
        )

        for uma_mensagem in mensagens_resposta["data"]:
            if "text" in uma_mensagem["content"]:
                print("\n")
                print(uma_mensagem["content"]["text"])
            elif "image_file" in uma_mensagem["content"]:
                resposta_da_openai = openai.File.retrieve(uma_mensagem["content"]["image_file"]["file_id"])
                image_data = openai.File.content(resposta_da_openai["id"])
                image_data_bytes = image_data.read()

                with open("grafico.png", "wb") as file:
                    file.write(image_data_bytes)
    else:
        print(run["status"])

    apagar_arquivo(arquivo["id"])
    apagar_thread(thread["id"])
    apagar_assistente(assistente["id"])

if __name__ == "__main__":
    main()