package com.example.cadastro.services
import com.example.cadastro.events.CadastroSolicitado
import com.example.cadastro.repositories.*
import jakarta.validation.Validator
import org.springframework.dao.DuplicateKeyException
import org.springframework.stereotype.Service
import java.util.UUID
@Service
class CadastroService(private val repository: ClienteRepository, private val validator: Validator) {
 fun processar(evento: CadastroSolicitado) {
  UUID.fromString(evento.requestId)
  require(validator.validate(evento.dados).isEmpty()) { "Dados de cadastro inválidos" }
  val d = evento.dados
  // requestId é o _id único: uma reentrega não cria outro documento.
  try { repository.insert(Cliente(evento.requestId, d.nome.trim(), d.email.trim(), d.cpf)) }
  catch (e: DuplicateKeyException) {
   val existente = repository.findById(evento.requestId).orElseThrow { e }
   require(existente == Cliente(evento.requestId, d.nome.trim(), d.email.trim(), d.cpf)) { "requestId reutilizado com dados diferentes" }
  }
 }
}
