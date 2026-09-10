package com.example.cadastro.configuration
import org.springframework.beans.factory.annotation.Value
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import software.amazon.awssdk.auth.credentials.*
import software.amazon.awssdk.regions.Region
import software.amazon.awssdk.services.sns.SnsClient
import software.amazon.awssdk.services.sqs.SqsClient
import java.net.URI
import java.time.Duration
import software.amazon.awssdk.core.client.config.ClientOverrideConfiguration
@Configuration
class MessagingConfiguration(@Value("\${lab.aws-endpoint}") private val endpoint: String) {
 private fun uri(): URI = URI.create(endpoint).also {
  require(it.host in setOf("localhost", "127.0.0.1", "localstack")) { "Este laboratório permite apenas emulação local" }
 }
 private val credentials = StaticCredentialsProvider.create(AwsBasicCredentials.create("test", "test"))
 @Bean fun sns(): SnsClient = SnsClient.builder().endpointOverride(uri()).region(Region.US_EAST_1).credentialsProvider(credentials).overrideConfiguration(ClientOverrideConfiguration.builder().apiCallTimeout(Duration.ofSeconds(8)).build()).build()
 @Bean fun sqs(): SqsClient = SqsClient.builder().endpointOverride(uri()).region(Region.US_EAST_1).credentialsProvider(credentials).overrideConfiguration(ClientOverrideConfiguration.builder().apiCallTimeout(Duration.ofSeconds(8)).build()).build()
}
