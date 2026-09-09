# Frontend Angular

Formulário didático em português para nome, e-mail e CPF. Angular 22.1.5,
CLI/build 22.1.7 e TypeScript 6.0.3. Runtime usado na validação: Node.js 24.19.0.

## Instalar e executar

Instale Node.js 24 LTS (24.15.0 ou superior da linha 24), que inclui npm.
Na pasta do repositório:

```sh
cd frontend
npm install
npm start
```

Abra http://localhost:4200. Para parar, Ctrl+C; para reiniciar, `npm start`.
O servidor escuta somente no computador local. Não precisa instalar Angular CLI global.

O ambiente Codex usou pnpm e inclui `pnpm-lock.yaml`. Para reproduzir esse conjunto
de versões com pnpm: `pnpm install --frozen-lockfile`, `pnpm start`.

```sh
npm run build
npm test
```

O build fica em `dist/cadastro/browser`. Testes unitários usam Vitest e jsdom,
sem abrir navegador.

## Demonstração e API

A configuração fica em `src/config/api.config.ts`:

```ts
export const apiConfig: ApiConfig = {
  demo: true,
  baseUrl: 'http://localhost:8080'
};
```

Com `demo: true`, o clique valida e exibe o JSON. Não existe envio HTTP,
armazenamento no navegador ou cadastro salvo. Use dados fictícios nos estudos.

Quando o backend estiver disponível, altere para `demo: false` e ajuste `baseUrl`.
Reinicie o servidor ou gere novo build após alterar a configuração. A URL deve
conter apenas a base da API; o serviço acrescenta `/clientes`. Configuração do
frontend é pública: nunca colocar chaves ou senhas.

Contrato preparado:

```http
POST /clientes
Content-Type: application/json

{
  "nome": "Cliente Exemplo",
  "email": "cliente@example.com",
  "cpf": "12345678901"
}
```

O CPF deve ter exatamente 11 dígitos sem pontuação; não há validação dos dígitos
verificadores nesta etapa. Todos os campos são obrigatórios, o nome não pode
conter apenas espaços e o e-mail passa pela validação do Angular.

O serviço espera `202 Accepted`, com corpo vazio ou JSON, e informa apenas que
a solicitação está pendente. Outros status, falhas de rede e timeout de 15 segundos
exibem erro sem limpar os dados. Não há retry automático nem confirmação de gravação.
A futura API deve configurar CORS para a origem usada, por exemplo
`http://localhost:4200` ou `http://127.0.0.1:4200`. Backend não faz parte desta entrega.

## Arquivos para estudar

- `src/pages/cadastro.page.ts`: formulário reativo, validação e estados.
- `src/pages/cadastro.page.html`: campos, mensagens e prévia.
- `src/services/cadastro.service.ts`: demonstração e integração HttpClient.
- `src/types/cadastro.ts`: contratos TypeScript.
- `src/config/api.config.ts`: seleção do modo e URL.
- `src/main.ts`: inicialização e configuração do HttpClient.
- `src/styles.css`: apresentação responsiva e foco do teclado.

As pastas `components` e `public` seguem reservadas. A tela é pequena e ainda não
precisa de componentes compartilhados.

Referências: [compatibilidade Angular](https://angular.dev/reference/versions) e
[requisições HttpClient](https://angular.dev/guide/http/making-requests).
