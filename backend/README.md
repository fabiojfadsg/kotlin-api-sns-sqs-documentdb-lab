# API Kotlin local

Spring Boot 4.1.1, Kotlin 2.3.21, Gradle Wrapper 9.7.1 e Java 24, usando o JDK
disponível nesta máquina. É uma aplicação didática vinculada a 127.0.0.1.

## Executar

Com Docker Desktop ativo, a partir da raiz:

```sh
docker compose -f infra/compose.yaml up -d --wait
cd backend
./gradlew test bootJar
./gradlew bootRun
```

API em http://127.0.0.1:8080. Em outro terminal, execute o frontend com `npm start`
na pasta frontend. Configuração pública: `frontend/src/config/api.config.ts`.

Para parar a API use Ctrl+C. Para parar o banco/emulador preservando o volume:

```sh
docker compose -f infra/compose.yaml stop
```

Para reiniciar, use `up -d --wait` e `./gradlew bootRun` novamente. Não use
`down -v`: isso excluiria os dados. MongoDB conserva os dados no volume nomeado;
a mensageria local é efêmera e recriada pelo script de inicialização em cada
início do emulador. Mensagens pendentes podem se perder ao reiniciar o emulador.

## Testar

```sh
curl -i http://127.0.0.1:8080/clientes -H 'Content-Type: application/json' \
  -d '{"nome":"Cliente Teste","email":"teste@example.com","cpf":"12345678901"}'
```

A resposta 202 contém `requestId` e `status: PENDENTE`. Consulte depois com
`GET /clientes/{requestId}`. Antes da gravação ou para ID desconhecido, retorna
404; não é um rastreador completo de falhas. Há também um teste integrado em
`devtools/testar-fluxo.py`: executar `python3 devtools/testar-fluxo.py` na raiz.

## Responsabilidades e contrato

Controller valida dados básicos e chama o producer, que serializa
CadastroSolicitado e publica no SNS. A assinatura entrega JSON bruto ao SQS.
O listener desserializa, chama o service, que valida e usa o repository MongoDB.
A confirmação (delete) no SQS ocorre somente após persistência bem-sucedida.
Falhas deixam a mensagem reaparecer após 30 s; após 3 recebimentos sem sucesso,
a política de redrive leva à cadastro-dlq. Não há reprocessamento automático da DLQ.

Nome não vazio, e-mail válido e CPF com 11 números são obrigatórios. Não se
calculam dígitos verificadores. requestId é o _id único: reentrega do mesmo evento
é idempotente; o mesmo ID com outro conteúdo falha. Duas novas requisições POST
com o mesmo CPF geram dois IDs e dois cadastros: unicidade de CPF não foi definida.
Não há retry automático no frontend. Um timeout pode ocorrer depois da publicação.

O GET é didático, sem autenticação. CORS aceita somente localhost:4200 e
127.0.0.1:4200. Não expor este ambiente à internet.

## Configuração

Variáveis opcionais: `PORT`, `MONGODB_URI`, `AWS_ENDPOINT`, `SQS_QUEUE_URL`.
Defaults estão em `src/main/resources/application.properties`. SNS/SQS usam
credenciais fictícias `test` e endpoint local obrigatório; não usam credenciais
reais ou a cadeia padrão AWS. Nunca versionar segredos.

MongoDB 8.0 é substituto didático do Amazon DocumentDB, não DocumentDB real e
não garante compatibilidade funcional ou operacional. LocalStack 4.0.3 é uma
versão fixada do emulador comunitário para este laboratório local, sem AWS real.

Referências: [Spring Boot](https://docs.spring.io/spring-boot/system-requirements.html),
[LocalStack](https://docs.localstack.cloud/aws/getting-started/installation/).
