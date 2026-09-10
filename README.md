# Laboratório de cadastro assíncrono de clientes

Projeto público educacional para aprender Kotlin e as responsabilidades de cada
camada, construindo uma etapa por vez. O frontend Angular funciona localmente. A API Kotlin e a infraestrutura local SNS/SQS + MongoDB estão implementadas.
Consulte [execução local completa](backend/README.md).

## Fluxo decidido

Tela Angular com nome, e-mail e CPF → `POST /clientes` → API Kotlin com Spring Boot →
`CadastroSolicitado` em JSON → SNS → SQS → consumidor Kotlin → serviço →
repositório → Amazon DocumentDB.

A API valida o básico e responde `202 Accepted` somente após a publicação ser
aceita pelo SNS. O cadastro permanece pendente: a API não grava o cliente antes
da fila. O consumidor desserializa a solicitação, chama o serviço para validar
regras de negócio e usa o repositório para salvar no DocumentDB.

![Arquitetura do cadastro](docs/images/arquitetura-cadastro.png)

## Organização inicial

- `frontend/`: tela, componentes, comunicação HTTP e tipos. Angular 22.
- `backend/`: pastas Kotlin para entrada HTTP, contratos, mensageria, serviços,
  persistência, configuração, erros e testes. API e consumidor podem compartilhar
  o mesmo microsserviço; a implantação será definida depois.
- `infra/`: espaço reservado para a futura infraestrutura.
- `devtools/`: espaço reservado para ferramentas do ambiente local.
- [Contexto e responsabilidades](docs/contexto.md): decisões, limites e próximos passos.
- [Documentação visual](docs/README.md) e [fonte Mermaid](docs/fluxo.mmd).

O frontend possui configuração, dependências e testes; as pastas do backend seguem
reservadas. Nunca versionar chaves, tokens, senhas ou outros segredos.

## Executar o frontend

Com Node.js 24.15 ou superior da linha 24 e npm instalados:

```sh
cd frontend
npm install
npm start
```

Abra http://localhost:4200. A integração com a API local é configurada em frontend/src/config/api.config.ts. Veja [instruções e configuração da API](frontend/README.md).

A imagem preservada abaixo pode omitir o CPF, adicionado posteriormente;
o contrato atual está no contexto e no Mermaid.

## Como continuar

Começar pela estrutura e pelos conceitos Kotlin, explicando cada arquivo antes de
avançar. Implementar primeiro uma pequena etapa verificável, depois integrar as
seguintes. Retentativas, DLQ, idempotência e consistência entre persistência e
publicação serão estudadas na evolução do laboratório.
