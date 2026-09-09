import { afterEach, describe, expect, it } from 'vitest';
import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { API_CONFIG } from '../config/api.config';
import { CadastroService } from './cadastro.service';
const payload = { nome: 'Ana', email: 'ana@example.com', cpf: '12345678901' };
function setup(demo: boolean) {
  TestBed.configureTestingModule({providers: [provideHttpClient(), provideHttpClientTesting(), {provide: API_CONFIG, useValue: {demo, baseUrl: 'http://localhost:8080/'}}]});
  return { service: TestBed.inject(CadastroService), http: TestBed.inject(HttpTestingController) };
}
afterEach(() => { TestBed.inject(HttpTestingController).verify(); TestBed.resetTestingModule(); });
describe('CadastroService', () => {
  it('demonstra sem enviar HTTP', () => {
    const {service, http} = setup(true);
    service.solicitar(payload).subscribe(r => expect(r).toEqual({modo: 'demonstracao', payload}));
    http.expectNone(() => true);
  });
  it('envia contrato e aceita 202 com corpo vazio', () => {
    const {service, http} = setup(false);
    service.solicitar(payload).subscribe(r => expect(r.modo).toBe('api'));
    const req = http.expectOne('http://localhost:8080/clientes');
    expect(req.request.method).toBe('POST'); expect(req.request.body).toEqual(payload);
    req.flush(null, {status: 202, statusText: 'Accepted'});
  });
  it('propaga falha HTTP sem confirmar cadastro', () => {
    const {service, http} = setup(false); let failed = false;
    service.solicitar(payload).subscribe({error: () => failed = true});
    http.expectOne('http://localhost:8080/clientes').flush(null, {status: 500, statusText: 'Error'});
    expect(failed).toBe(true);
  });
  it('rejeita status diferente do contrato 202', () => {
    const {service, http} = setup(false); let failed = false;
    service.solicitar(payload).subscribe({error: () => failed = true});
    http.expectOne('http://localhost:8080/clientes').flush({}); expect(failed).toBe(true);
  });
});
