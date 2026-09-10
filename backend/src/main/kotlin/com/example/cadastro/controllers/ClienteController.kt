package com.example.cadastro.controllers
import com.example.cadastro.dtos.CadastroRequest
import com.example.cadastro.events.CadastroSolicitado
import com.example.cadastro.messaging.producers.CadastroProducer
import com.example.cadastro.repositories.ClienteRepository
import jakarta.validation.Valid
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*
import org.springframework.web.server.ResponseStatusException
import org.springframework.http.HttpStatus
import java.util.UUID
@RestController
@RequestMapping("/clientes")
@CrossOrigin(origins = ["http://localhost:4200", "http://127.0.0.1:4200"])
class ClienteController(private val producer: CadastroProducer, private val repository: ClienteRepository) {
 @PostMapping fun solicitar(@Valid @RequestBody dados: CadastroRequest): ResponseEntity<Map<String,String>> {
  val id = UUID.randomUUID().toString()
  producer.publicar(CadastroSolicitado(id, dados))
  return ResponseEntity.accepted().body(mapOf("requestId" to id, "status" to "PENDENTE"))
 }
 @GetMapping("/{id}") fun consultar(@PathVariable id: String) = repository.findById(id).orElseThrow {
  ResponseStatusException(HttpStatus.NOT_FOUND, "Cadastro ainda não persistido ou desconhecido")
 }
}
