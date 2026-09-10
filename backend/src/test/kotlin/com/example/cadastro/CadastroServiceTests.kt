package com.example.cadastro
import com.example.cadastro.dtos.CadastroRequest
import com.example.cadastro.events.CadastroSolicitado
import com.example.cadastro.repositories.*
import com.example.cadastro.services.CadastroService
import jakarta.validation.Validation
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.Assertions.*
import org.mockito.Mockito.*
import org.springframework.dao.DuplicateKeyException
import java.util.Optional
import java.util.UUID
class CadastroServiceTests {
 private val repository = mock(ClienteRepository::class.java)
 private val validator = Validation.buildDefaultValidatorFactory().validator
 private val service = CadastroService(repository, validator)
 private val id = UUID.randomUUID().toString()
 @Test fun `dados invalidos nao chegam ao banco`() {
  assertThrows(IllegalArgumentException::class.java) { service.processar(CadastroSolicitado(id, CadastroRequest(" ", "invalido", "1"))) }
  verifyNoInteractions(repository)
 }
 @Test fun `salva solicitacao valida`() {
  val cliente = Cliente(id,"Ana","ana@example.com","12345678901")
  `when`(repository.insert(cliente)).thenReturn(cliente)
  service.processar(CadastroSolicitado(id,CadastroRequest(cliente.nome,cliente.email,cliente.cpf)))
  verify(repository).insert(cliente)
 }
 @Test fun `reentrega do mesmo evento e idempotente`() {
  val cliente = Cliente(id,"Ana","ana@example.com","12345678901")
  `when`(repository.insert(cliente)).thenThrow(DuplicateKeyException("duplicado"))
  `when`(repository.findById(id)).thenReturn(Optional.of(cliente))
  assertDoesNotThrow { service.processar(CadastroSolicitado(id,CadastroRequest(cliente.nome,cliente.email,cliente.cpf))) }
 }
}
