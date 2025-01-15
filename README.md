# VERZEL - **Developer Allocation API**  

## Overview
A Developer Allocation API é uma aplicação escrita em Django, projetada para gerenciar e realizar a alocação de desenvolvedores de software em projetos. 
O principal objetivo da API é assegurar que os gerentes de projeto possam alocar desenvolvedores de forma eficiente, levando em conta suas especializações e as necessidades dos projetos.

## Instalation
A aplicação utiliza Docker Compose para facilitar a configuração e execução. O processo envolve a inicialização de um banco de dados PostgreSQL 15 e da aplicação Django, juntamente com as dependências necessárias para a execução da aplicação.

### Passos para Instalação
1. Certifique-se de ter o **Docker** e o **Docker Compose** instalados no seu ambiente.
2. Clone o repositório do projeto:
   ```bash
   git clone git@github.com:Ch3did/verzel.git
   cd verzel/
3. Execute o comando para iniciar o ambiente:
   ```bash
   docker-compose up -d --build


## First Usage 

Após a instalação, a aplicação estará disponível no endereço: http://localhost:8000. Você pode verificar seu funcionamento acessando a rota **/health**. Todas as demais rotas da aplicação são protegidas por autenticação JWT. Para obter um token, acesse a rota **/token**. Caso ainda não tenha um usuário, será necessário registrá-lo através da rota **/register**.

### **Como Usar o Token JWT**

1. **Após obter o token de acesso**, envie-o no cabeçalho de cada requisição para endpoints protegidos:
   - **Header**:
     ```
     Authorization: Bearer <seu_access_token>
     ```

2. **Exemplo de Requisição Autenticada**:
   ```bash
   curl -X GET "http://localhost:8000/api/protected-endpoint/" \
        -H "Authorization: Bearer <seu_access_token>"
   ```

## Endpoints


### 1. Listagem de Alocações - /alocacoes/

- **Endpoint**: /api/alocacoes/
- **Métodos** Aceitos: GET
- **Descrição**: Retorna a lista de todas as alocações, com informações detalhadas sobre os programadores e projetos alocados.

### 2. Criar Alocação - /alocacoes/

- **Endpoint**: /api/alocacoes/
- **Métodos** Aceitos: POST
- **Descrição**: Cria uma nova alocação associando programadores a um projeto, com a possibilidade de definir as horas alocadas.
- **Parâmetros**: Deve ser enviado no corpo da requisição o projeto_id, programadores_id, e opcionalmente as horas.

### 3. Atualizar Alocação - /alocacoes/{id}/

- **Endpoint**: /api/alocacoes/{id}/
- **Métodos** Aceitos: PUT
- **Descrição**: Atualiza os dados de uma alocação existente, incluindo a associação de programadores e o número de horas.
- **Parâmetros**: O ID da alocação deve ser especificado na URL, e os dados a serem atualizados no corpo da requisição.

### 4. Atualizar Parciais de Alocação - /alocacoes/{id}/

- **Endpoint**: /api/alocacoes/{id}/
- **Métodos** Aceitos: PATCH
- **Descrição**: Atualiza parcialmente os dados de uma alocação, permitindo a modificação de programadores ou horas alocadas.
- **Parâmetros**: O ID da alocação deve ser especificado na URL e os campos a serem atualizados no corpo da requisição.

### 5. Excluir Alocação - /alocacoes/{id}/

- **Endpoint**: /api/alocacoes/{id}/
- **Métodos** Aceitos: DELETE
- **Descrição**: Exclui uma alocação existente, removendo-a da base de dados.
- **Parâmetros**: O ID da alocação a ser excluída deve ser especificado na URL.

### 6. Listar Programadores - /programadores/

- **Endpoint**: /api/programadores/
- **Métodos** Aceitos: GET
- **Descrição**: Retorna a lista de todos os programadores cadastrados.

### 7. Criar Programador - /programadores/

- **Endpoint**: /api/programadores/
- **Métodos** Aceitos: POST
- **Descrição**: Cria um novo programador com as informações fornecidas, como nome e tecnologias associadas.
- **Parâmetros**: No corpo da requisição deve ser enviado o nome do programador e as tecnologias.

### 8. Atualizar Programador - /programadores/{id}/

- **Endpoint**: /api/programadores/{id}/
- **Métodos** Aceitos: PUT, PATCH
- **Descrição**: Atualiza os dados de um programador, como nome e tecnologias associadas.
- **Parâmetros**: O ID do programador deve ser especificado na URL, e os dados a serem atualizados no corpo da requisição.

### 9. Excluir Programador - /programadores/{id}/

- **Endpoint**: /api/programadores/{id}/
- **Métodos** Aceitos: DELETE
- **Descrição**: Exclui um programador existente.
- **Parâmetros**: O ID do programador a ser excluído deve ser especificado na URL.

### 10. Listar Projetos - /projetos/

- **Endpoint**: /api/projetos/
- **Métodos** Aceitos: GET
- **Descrição**: Retorna a lista de todos os projetos cadastrados.

### 11. Criar Projeto - /projetos/

- **Endpoint**: /api/projetos/
- **Métodos** Aceitos: POST
- **Descrição**: Cria um novo projeto com as informações fornecidas, como nome e horas disponíveis por dia.
- **Parâmetros**: No corpo da requisição devem ser enviados o nome do projeto e as horas disponíveis por dia.

### 12. Atualizar Projeto - /projetos/{id}/

- **Endpoint**: /api/projetos/{id}/
- **Métodos** Aceitos: PUT, PATCH
- **Descrição**: Atualiza os dados de um projeto, como nome e horas disponíveis por dia.
- **Parâmetros**: O ID do projeto deve ser especificado na URL, e os dados a serem atualizados no corpo da requisição.

### 13. Excluir Projeto - /projetos/{id}/

- **Endpoint**: /api/projetos/{id}/
- **Métodos**: DELETE
- **Descrição**: Exclui um projeto existente.
- **Parâmetros**: O ID do projeto a ser excluído deve ser especificado na URL.

### 14. Cadastro de Usuário - /register

- **Endpoint**: `/api/users/register/`
- **Métodos**: `POST`
- **Descrição**: Cria um novo usuário no sistema.

### 15. Autenticação (Obter Tokens JWT) - /token/

- **Endpoint**: `/api/token/`
- **Métodos**: `POST`
- **Descrição**: Gera tokens JWT (access e refresh) para autenticar o usuário.
authorized`: Credenciais inválidas.

### 16. Atualizar o Token de Acesso (Refresh Token) - token/refresh/

- **Endpoint**: `/api/token/refresh/`
- **Métodos**:`POST`
- **Descrição**: Atualiza o token de acesso usando o token de refresh.


## Opinions and Contributions

Contribuições e feedback são bem-vindos para melhorar a VERZEL - Developer Allocation API. Se você tiver ideias, sugestões ou encontrar algum problema, siga as orientações abaixo:

### Como Contribuir
1. Faça um fork deste repositório.
2. Crie uma nova branch para sua contribuição:
   ```bash
   git checkout -b minha-contribuicao
   ```
3. Faça as alterações necessárias e adicione comentários claros no código.
4. Envie um pull request descrevendo sua contribuição.
