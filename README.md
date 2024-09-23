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

Se você receber uma mensagem de erro afirmando que o módulo "app" não existe, talvez seja um problema de PYTHONPATH.
Para resolver esse problema em ambientes bash, rode o script pythonpath.sh na raíz do projeto:

`bash pythonpath.sh`


# Rotas

POST - /vehicles - Cria um novo veículo. A criação requer os campos seguintes: name, brand, year. Retornando com status 201 os seguintes campos: name, brand, year, id, created_at, updated_at.

GET - Lista os veículos. A listagem obedece uma regra de paginação de no máximo 50 veículos por requisição. O retorno com status 200 traz uma lista de no máximo 50 dicionários contendo, cada um, os seguintes campos: name, brand, year, id, created_at, updated_at.

GET - /vehicles/{id} - Lista os detalhes de um veículo particular. É necessário passar o parâmetro id pelo método GET do protocolo HTTP. Serão retornados com status 200 os seguintes campos do veículo específico: name, brand, year, id, created_at, updated_at.

# Documentação

Abra seu navegador e acesse o endereço http://127.0.0.1:8000/docs. Você verá a interface interativa do Swagger UI, onde poderá explorar a documentação da API.


# Testes

### Testes Automatizados

Os testes automatizados podem ser executados com o pytest, usando o seguinte comando:

`pytest`

### Testes manuais

A API também pode ser testada usando clientes especializados, como Postman e Insomnia.

Se você utiliza o vscode, uma forma alternativa de testar as rotas é executando a extensão REST Cli enviando requisições com através da manipulação do arquivo .http

# Pontos de Melhoria

- Emular um banco de dados para testes (atualmente os testes rodam no mesmo banco de dados real da API)
- Usar um linter
- Usar atalhos para linhas de comandos (rodar aplicação, rodar testes)
- Criar manifestos para deploy no Kubernetes