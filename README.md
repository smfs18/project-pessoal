# Implementação de um Agente de Triagem Utilizando Lang Graph

## Descrição

[cite_start]Este projeto consiste no desenvolvimento de um sistema de triagem de emergência baseado em uma arquitetura cliente-servidor[cite: 2]. [cite_start]O sistema utiliza um agente de IA para interagir com o usuário, analisar o contexto das mensagens para identificar emergências e garantir que todas as informações necessárias para a triagem sejam coletadas[cite: 2].

[cite_start]O frontend da aplicação se comunica com o backend através de requisições HTTP[cite: 2]. [cite_start]Um agente de triagem inteligente recebe a mensagem do usuário e, com o auxílio de outro agente, analisa o contexto para tomar decisões[cite: 2]. [cite_start]Após a conclusão da triagem, um terceiro agente é acionado para extrair e organizar um sumário das informações coletadas[cite: 2]. [cite_start]Todas as interações são salvas em um banco de dados para manter o histórico e permitir que a IA "lembre" das conversas anteriores[cite: 3].

## Features

* [cite_start]**Agente de Triagem Inteligente:** Utiliza Lang Graph para analisar mensagens, identificar emergências e conduzir o processo de triagem[cite: 1, 2].
* [cite_start]**Extração de Sumário:** Um agente dedicado organiza as informações da triagem após a sua finalização[cite: 2].
* [cite_start]**Persistência de Dados:** Cada mensagem, seja do usuário ou do agente, é salva no banco de dados para garantir a continuidade da conversa[cite: 3].
* [cite_start]**Reconhecimento Óptico de Caracteres (OCR):** O backend possui uma função que utiliza EasyOCR para ler imagens e reconhecer caracteres[cite: 4].
* [cite_start]**Testes Unitários:** A aplicação conta com testes unitários desenvolvidos com Pytest para garantir a qualidade e o funcionamento esperado[cite: 5].

## Tecnologias Utilizadas

* [cite_start]**Backend:** Python (FastAPI e uvicorn) [cite: 7]
* [cite_start]**Frontend:** HTML, CSS e JavaScript [cite: 8]
* [cite_start]**Banco de Dados:** MongoDB [cite: 9]
* [cite_start]**Agente:** Lang Graph [cite: 10]
* [cite_start]**Testes:** Pytest [cite: 11]

## Estrutura do Projeto

A estrutura de diretórios e arquivos do projeto está organizada da seguinte forma:
├── app/
│   ├── db/
│   │   ├── database.py
│   │   └── models.py
│   ├── routes/
│   │   └── webhook.py
│   ├── services/
│   │   ├── llm_client.py
│   │   └── triage_agent.py
│   └── utils/
│       └── emergency.py
├── Frontend/
├── teste/
│   ├── test_emergency.py
│   ├── test_llm_client.py
│   └── test_webhook.py
├── venv/
├── .env
├── .gitignore
├── main.py
├── pytest.ini
└── requirements.txt

[cite_start][cite: 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42]

## Como Rodar o Projeto

Siga os passos abaixo para executar a aplicação:
1.  Instalar todas as bibliotecas do requirements.txt
    ```bash
       pip install -r requirements.txt
    ```
2.  [cite_start]**Abrir o Frontend:** Abra o arquivo HTML do frontend em qualquer navegador[cite: 44].
3.  **Ativar o Ambiente Virtual:** Ative o `venv` com o seguinte comando:
    ```bash
    source venv/bin/activate
    ```
    [cite_start][cite: 45]
4.  **Ligar o Servidor:** Inicie o servidor backend:
    ```bash
    uvicorn main:app --reload
    ```
    [cite_start][cite: 46]
5.  **Ativar o Banco de Dados:** Inicie o container do MongoDB:
    ```bash
    docker start clinicai-mongo
    ```
    [cite_start][cite: 47]

