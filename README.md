# PetSchool

Aplicação web para cadastro e consulta de tutores e pets. O frontend em Vue.js
consome uma API FastAPI, que persiste os dados em um banco MySQL.

## Tecnologias

- Vue.js 3;
- Vite;
- Vue Router;
- Bootstrap 5;
- Bootstrap Icons;
- FastAPI;
- MySQL.

## Pré-requisitos

Antes de iniciar, verifique se estão instalados:

- [Node.js](https://nodejs.org/);
- npm;
- Python 3.10 ou superior;
- MySQL Server;
- [Git](https://git-scm.com/);
- [Visual Studio Code](https://code.visualstudio.com/), recomendado.

O projeto utiliza o Node.js `22.18.0`, definido no arquivo `.nvmrc`.

```bash
node --version
npm --version
git --version
```

Caso utilize NVM no Linux ou macOS:

```bash
nvm install
nvm use
```

No Windows com `nvm-windows`:

```powershell
nvm install 22.18.0
nvm use 22.18.0
```

## Instalação

Na raiz do projeto, instale as dependências do frontend:

```bash
npm install
```

## Execução

Inicie o servidor de desenvolvimento:

```bash
npm run dev
```

O terminal apresentará o endereço local da aplicação, normalmente:

```text
http://localhost:5173
```

Para configurar o MySQL e iniciar a API, siga as instruções em
[backend/README.md](./backend/README.md).

Outros comandos disponíveis:

```bash
npm run format
npm run lint
npm run build
npm run preview
```

## Estrutura do projeto

A aplicação organiza páginas, componentes, serviços, rotas e estilos por
responsabilidade.

## Documentação

- [Configuração do projeto](./docs/02-configuracao-projeto.md);
- [Layout do PetSchool](./docs/03-layout-petschool.md);
- [Criação das views](./docs/04-criar-views.md);
- [Listagem de pets](./docs/05-ListarPets.md);
- [Guia de padronização do código](./docs/guia-padronizacao-codigo.md);
- [Testes da API e preparação do MySQL](./backend/README.md).

## API FastAPI da atividade

O backend solicitado na atividade, com acesso ao MySQL e instruções para o
Workbench, está em [backend/README.md](./backend/README.md).

## Contribuição

Para contribuir:

1. faça um fork, caso não possua acesso direto ao repositório;
2. clone o repositório ou seu fork;
3. crie uma branch para a alteração;
4. desenvolva e teste a funcionalidade;
5. execute a formatação, o lint e o build;
6. crie um commit com uma mensagem descritiva;
7. envie a branch ao GitHub;
8. abra um Pull Request.

```bash
git switch -c feat/nome-da-funcionalidade
npm run format
npm run lint
npm run build
git add .
git commit -m "feat: adiciona nova funcionalidade"
git push origin feat/nome-da-funcionalidade
```

## Origem do template

Este projeto foi iniciado a partir do
[Template Vue.js com Bootstrap](https://github.com/ifc-dev-web2/tec-vue-bootstrap-template),
desenvolvido pelo
[Prof. Cristofer Sousa](https://github.com/cristofersousa) para atividades de
Desenvolvimento Web do Instituto Federal Catarinense — Campus Araquari.

## Licença

Consulte os termos de utilização no arquivo [LICENSE](LICENSE).
