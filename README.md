# msx-api-001
Uma API RESTful em Python, utilizando FastAPI, que permite a criação, leitura, atualização e deleção de registros de veículos, com funcionalidades básicas de autenticação e documentação automática.

# Instalação

Para montar um ambiente de desenvolvimento local você pode utilizar as ferramentas populares: venv e pip.

Com o instalado na sua máquina, execute o comando no diretório raiz:

`python -m venv .venv`

Depois disso, pressupondo que você está em um sistema Linux, é necessário carregar o ambiente virtual:

`source .venv/bin/activate` 

Agora você está em um ambiente isolado propício para instalar as dependências do projeto:

`python -m pip install -r requirements.txt`

Por fim, rode o servidor web em ambiente de desenvolvimento para testar:

`fastapi dev app/main.py`

# Documentação

Abra seu navegador e acesse o endereço http://127.0.0.1:8000/docs. Você verá a interface interativa do Swagger UI, onde poderá explorar a documentação da API.


# Testes

Os testes automatizados podem ser executados com o pytest, usando o seguinte comando:

`pytest`

Se você utiliza o vscode, uma forma alternativa de testar as rotas é executando a extensão REST Cli enviando requisições com através do arquivo .http

# Rotas

POST - /vehicles - Cria um novo veículo. A criação requer os campos seguintes: name, brand, year. Retornando com status 201 os seguintes campos: name, brand, year, id, created_at, updated_at.

GET - Lista os veículos. A listagem obedece uma regra de paginação de no máximo 50 veículos por requisição. O retorno com status 200 traz uma lista de no máximo 50 dicionários contendo, cada um, os seguintes campos: name, brand, year, id, created_at, updated_at.

GET - /vehicles/{id} - Lista os detalhes de um veículo particular. É necessário passar o parâmetro id pelo método GET do protocolo HTTP. Serão retornados com status 200 os seguintes campos do veículo específico: name, brand, year, id, created_at, updated_at.