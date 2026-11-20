# Estudo: funções assíncronas

## O que é uma função assíncrona? 

É uma função que pode aguardar uma operação sem bloquear a página. Buscar dados depende do tempo de resposta da rede e do servidor, que pode variar.

## O que é uma Promise e quais são seus estados?

Uma `Promise` representa o resultado futuro de uma operação. Seus estados são **pending** (aguardando), **fulfilled** (concluída com sucesso) e **rejected** (concluída com erro).

## Para que servem `async` e `await`? 

`async` declara uma função assíncrona e faz com que ela retorne uma `Promise`. `await` aguarda essa Promise: a função fica suspensa naquele ponto, mas a página continua funcionando. Depois, a função retoma a execução.

## O que faz a Fetch API? Qual a diferença entre `fetch(url)` e `resposta.json()`?

`fetch(url)` faz a requisição e retorna uma Promise com a resposta HTTP. `resposta.json()` lê o conteúdo da resposta e o converte de JSON para dados JavaScript; também retorna uma Promise.

Uma resposta HTTP com erro não faz necessariamente o `fetch` falhar. Por isso, no projeto verificamos `resposta.ok` antes de chamar `.json()`.

## Como tratar erros da API?

No projeto, `try/catch` trata falhas de rede, respostas HTTP inválidas e JSON inválido. Também verificamos se os dados recebidos são uma lista. O `finally` encerra o carregamento, e a tela mostra uma mensagem de erro quando necessário.
