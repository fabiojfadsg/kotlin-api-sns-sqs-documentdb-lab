package com.example.cadastro
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication
import org.springframework.scheduling.annotation.EnableScheduling
@SpringBootApplication
@EnableScheduling
class CadastroApplication
fun main(args: Array<String>) { runApplication<CadastroApplication>(*args) }
