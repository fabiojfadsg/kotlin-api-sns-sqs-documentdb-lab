import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { defer, map, Observable, of, timeout } from 'rxjs';
import { API_CONFIG } from '../config/api.config';
import { CadastroRequest, CadastroResultado } from '../types/cadastro';

@Injectable({ providedIn: 'root' })
export class CadastroService {
  private readonly http = inject(HttpClient);
  private readonly config = inject(API_CONFIG);

  solicitar(payload: CadastroRequest): Observable<CadastroResultado> {
    if (this.config.demo) return defer(() => of({ modo: 'demonstracao' as const, payload }));
    return this.http.post<unknown>(`${this.config.baseUrl.replace(/\/$/, '')}/clientes`, payload, { observe: 'response' }).pipe(
      timeout(15000),
      map(response => {
        if (response.status !== 202) throw new Error('Resposta inesperada: a API deve retornar 202 Accepted.');
        return { modo: 'api' as const, payload };
      })
    );
  }
}
