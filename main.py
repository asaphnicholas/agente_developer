
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st
import os

load_dotenv()

OPENAI_KEY = os.getenv('openai_key')

# Cria uma instância do cliente OpenAI
client = OpenAI(api_key=OPENAI_KEY)

# Define o modelo e a função principal do chatbot
def chatbot(query):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Escolha o modelo desejado
        messages=[
            {"role": "system", "content": "Você é um especialista em programação e desenvolvimento de software com amplo conhecimento em linguagens, frameworks, ferramentas, e boas práticas de engenharia de software. Sua missão é ajudar desenvolvedores a resolver dúvidas técnicas, oferecer sugestões claras e eficientes de código, explicar conceitos complexos de forma acessível e detalhada, além de fornecer orientações práticas para problemas do dia a dia no desenvolvimento. Você é preciso, objetivo e adaptável, ajustando suas respostas ao nível de experiência do usuário, seja iniciante ou avançado. Quando necessário, forneça exemplos de código bem comentados e explique passo a passo como eles funcionam. Evite respostas vagas e busque sempre ser didático e completo, mas sem ser excessivamente prolixo."},
            {"role": "user", "content": query}
        ]
    )
    # Retorna a resposta do assistente
    return completion.choices[0].message.content

# Função principal do Streamlit
def main():
    # Inicializa o histórico de mensagens
    if 'mensagens' not in st.session_state:
        st.session_state.mensagens = []

    mensagens = st.session_state.mensagens

    # Título do chat
    st.header("👨‍💻🤖 Assistente de Programação")

    # Renderiza as mensagens anteriores
    for mensagem in mensagens:
        chat = st.chat_message(mensagem['role'])
        chat.markdown(mensagem['content'])

    # Entrada do usuário
    message = st.chat_input("Digite sua mensagem")
    if message:
        # Adiciona a mensagem do usuário ao histórico
        nova_mensagem = {'role': 'user', 'content': message}
        mensagens.append(nova_mensagem)

        chat = st.chat_message('user')
        chat.markdown(message)

        # Envia a mensagem ao chatbot e recebe a resposta
        resposta = chatbot(message)

        # Adiciona a resposta do chatbot ao histórico
        resposta_mensagem = {'role': 'assistant', 'content': resposta}
        mensagens.append(resposta_mensagem)

        chat = st.chat_message('assistant')
        chat.markdown(resposta)

        # Atualiza o histórico na sessão
        st.session_state.mensagens = mensagens

# Executa a aplicação
if __name__ == '__main__':
    main()