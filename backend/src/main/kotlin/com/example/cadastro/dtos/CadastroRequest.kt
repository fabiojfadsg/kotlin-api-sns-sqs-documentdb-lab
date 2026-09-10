package com.example.cadastro.dtos
import jakarta.validation.constraints.*
data class CadastroRequest(
 @field:NotBlank val nome: String,
 @field:NotBlank @field:Email val email: String,
 @field:Pattern(regexp = "[0-9]{11}") val cpf: String
)
