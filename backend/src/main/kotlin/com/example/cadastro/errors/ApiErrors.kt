package com.example.cadastro.errors
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*
import software.amazon.awssdk.core.exception.SdkException
@RestControllerAdvice
class ApiErrors {
 @ExceptionHandler(SdkException::class)
 fun publicacaoIndisponivel(e: SdkException) = ResponseEntity.status(503).body(mapOf("erro" to "Não foi possível confirmar a publicação da solicitação."))
}
