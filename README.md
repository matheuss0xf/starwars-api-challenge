# Challenge Star Wars - API

Esta é uma API construída com FastAPI que permite a interação com o universo de Star Wars. A API oferece dois principais recursos:

1. **Consulta de Recursos**: Permite buscar informações sobre pessoas, planetas, espécies, filmes, naves e veículos.
2. **Perguntas sobre Star Wars**: Permite que o usuário faça perguntas sobre o universo Star Wars, e a API tentará responder com base em um conjunto de perguntas pré-definidas.

## Funcionalidades

### 1. Busca de Recursos do Star Wars

- **Endpoint**: `GET /{resource}`
- **Parâmetros**:
  - `resource` (path): O tipo de recurso que deseja consultar. Deve ser um dos seguintes: `people`, `planets`, `species`, `films`, `starships`, `vehicles`.
  - `page` (query): O número da página para consulta (padrão é 1).
  - `search` (query): Um termo opcional para filtrar os resultados pelo nome/título.
  
- **Exemplo de Requisição**:

  `GET /people?page=1&search=Luke`

  **Exemplo de Resposta**:
    ```json
    {
      "page": 1,
      "total_items": 1,
      "next": null,
      "previous": null,
      "results": [
        {
          "name": "Luke Skywalker",
          "height": "172",
          "mass": "77",
          "hair_color": "blond",
          "skin_color": "fair",
          "eye_color": "blue",
          "birth_year": "19BBY",
          "gender": "male",
          "homeworld": "Tatooine",
          "films": [
            "A New Hope",
            "The Empire Strikes Back",
            "Return of the Jedi"
          ]
        }...
      ]
    }
    ```
### 2. Perguntar sobre Star Wars
- Endpoint: POST /ask
- Parâmetros:
  - question (body): A pergunta que deseja fazer sobre o universo Star Wars. 
- Exemplo de Requisição:
```json
{
  "question": "Qual é o planeta natal de Luke Skywalker?"
}
```
- Exemplo de Resposta:
```json
{
  "message": "Tatooine."
}
```

## Tecnologias Utilizadas
- Poetry: Gerenciador de dependências e ambiente virtual.
- Taskpy: Criar atalhos para rodar comandos.
- Ruff: Formatação de código.
- FastAPI: Framework para construir APIs rápidas e modernas.
- spaCy: Biblioteca de processamento de linguagem natural (NLP).
- RapidFuzz: Para encontrar a melhor correspondência de perguntas.
- httpx: Cliente HTTP assíncrono para fazer requisições.
- pydantic: Para validação de dados.
- python-dotenv: Para carregar variáveis de ambiente.

## Instalação

1. **Clone o repositório**:

    ```bash
    git clone https://github.com/matheuss0xf/starwars-api.git
    cd starwars-api
    ```

2. **Instale as dependências**:

   `Poetry`:

   ```bash
   poetry install
   ```
    ```python -m spacy download pt_core_news_sm```
3. **Inicie a aplicação**:

    ```bash
    task run
    ```

4. **Acesse a documentação da API**:

    Após a aplicação iniciar, você pode acessar a documentação interativa da API no navegador:

    ```
    http://localhost:8000/docs
    ```

## Estrutura do Projeto

O projeto está estruturado da seguinte forma:

```
starwars-api/
├── app/
│   ├── controllers/
│   │   └── starwars_controller.py      # Controladores da API
│   ├── services/
│   │   └── question_processing_service.py  # Lógica de processamento de perguntas
│   │   └── swapi_service.py           # Lógica de integração com a API SWAPI
│   ├── assets/
│   │   └── questions.json             # Dados de perguntas
│   ├── __init__.py                    # Pacote Python
├── poetry.lock
├── pyproject.toml
├── README.md
├── main.py                        # Inicializador da aplicação
├── config.py                    # Configurações do projeto
└── .env   
```

## Como Funciona

1. **Pré-processamento das perguntas**:
    - O texto da pergunta é normalizado e processado, removendo caracteres especiais e convertendo para minúsculas.

2. **Extração de entidades**:
    - Através do `spaCy`, as entidades de interesse (personagens, planetas, etc.) são extraídas da pergunta.

3. **Correspondência com a base de dados de perguntas**:
    - Usamos a biblioteca `RapidFuzz` para realizar a correspondência de palavras-chave entre a pergunta e a base de dados interna.

4. **Busca de informações na SWAPI**:
    - Uma vez identificada a entidade, buscamos informações relevantes na API SWAPI.

### Executando o projeto:
