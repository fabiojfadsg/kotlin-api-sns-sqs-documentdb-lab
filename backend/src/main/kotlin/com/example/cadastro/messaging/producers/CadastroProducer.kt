package com.example.cadastro.messaging.producers
import com.example.cadastro.events.CadastroSolicitado
import org.springframework.beans.factory.annotation.Value
import org.springframework.stereotype.Component
import software.amazon.awssdk.services.sns.SnsClient
import tools.jackson.databind.ObjectMapper
@Component
class CadastroProducer(private val sns: SnsClient, private val mapper: ObjectMapper,
 @Value("\${lab.topic-arn}") private val topic: String) {
 fun publicar(evento: CadastroSolicitado) {
  sns.publish { it.topicArn(topic).message(mapper.writeValueAsString(evento)) }
 }
}
