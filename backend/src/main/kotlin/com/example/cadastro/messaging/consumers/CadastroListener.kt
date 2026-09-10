package com.example.cadastro.messaging.consumers
import com.example.cadastro.events.CadastroSolicitado
import com.example.cadastro.services.CadastroService
import org.slf4j.LoggerFactory
import org.springframework.beans.factory.annotation.Value
import org.springframework.stereotype.Component
import org.springframework.scheduling.annotation.Scheduled
import software.amazon.awssdk.services.sqs.SqsClient
import tools.jackson.databind.ObjectMapper
@Component
class CadastroListener(private val sqs: SqsClient, private val mapper: ObjectMapper,
 private val service: CadastroService, @Value("\${lab.queue-url}") private val queue: String) {
 private val log = LoggerFactory.getLogger(javaClass)
 @Scheduled(fixedDelay = 1000)
 fun consumir() {
  try {
   val mensagens = sqs.receiveMessage { it.queueUrl(queue).maxNumberOfMessages(5).waitTimeSeconds(2).visibilityTimeout(30) }.messages()
   for (m in mensagens) {
    try {
     service.processar(mapper.readValue(m.body(), CadastroSolicitado::class.java))
     sqs.deleteMessage { it.queueUrl(queue).receiptHandle(m.receiptHandle()) }
    } catch (e: Exception) { log.warn("Mensagem {} não concluída; será tentada novamente ({})", m.messageId(), e.javaClass.simpleName) }
   }
  } catch (e: Exception) { log.warn("Fila local indisponível ({})", e.javaClass.simpleName) }
 }
}
