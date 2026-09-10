package com.example.cadastro.repositories
import org.springframework.data.annotation.Id
import org.springframework.data.mongodb.core.mapping.Document
import org.springframework.data.mongodb.repository.MongoRepository
@Document("clientes")
data class Cliente(@Id val requestId: String, val nome: String, val email: String, val cpf: String)
interface ClienteRepository : MongoRepository<Cliente, String>
