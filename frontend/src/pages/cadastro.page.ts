import { Component, inject, signal } from '@angular/core';
import { JsonPipe } from '@angular/common';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { finalize } from 'rxjs';
import { API_CONFIG } from '../config/api.config';
import { CadastroService } from '../services/cadastro.service';
import { CadastroRequest, CadastroResultado } from '../types/cadastro';

@Component({ selector: 'app-root', standalone: true, imports: [ReactiveFormsModule, JsonPipe], templateUrl: './cadastro.page.html' })
export class CadastroPage {
  readonly config = inject(API_CONFIG);
  private readonly service = inject(CadastroService);
  readonly enviando = signal(false);
  readonly erro = signal('');
  readonly resultado = signal<CadastroResultado | null>(null);
  readonly form = new FormGroup({
    nome: new FormControl('', { nonNullable: true, validators: [Validators.required, Validators.pattern(/\S/)] }),
    email: new FormControl('', { nonNullable: true, validators: [Validators.required, Validators.email] }),
    cpf: new FormControl('', { nonNullable: true, validators: [Validators.required, Validators.pattern(/^\d{11}$/)] })
  });
  invalido(campo: keyof CadastroRequest): boolean {
    const control = this.form.controls[campo];
    return control.invalid && control.touched;
  }
  enviar(): void {
    if (this.enviando()) return;
    this.erro.set('');
    this.resultado.set(null);
    this.form.markAllAsTouched();
    if (this.form.invalid) { this.erro.set('Revise os campos indicados antes de continuar.'); return; }
    const value = this.form.getRawValue();
    const payload: CadastroRequest = { nome: value.nome.trim(), email: value.email.trim(), cpf: value.cpf };
    this.enviando.set(true);
    this.service.solicitar(payload).pipe(finalize(() => this.enviando.set(false))).subscribe({
      next: result => this.resultado.set(result),
      error: () => this.erro.set('Não foi possível confirmar o recebimento da solicitação. Verifique a conexão e a API antes de tentar novamente.')
    });
  }
}
