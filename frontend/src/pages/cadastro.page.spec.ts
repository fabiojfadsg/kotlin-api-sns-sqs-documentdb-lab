import { afterEach, expect, it, vi } from 'vitest';
import { TestBed } from '@angular/core/testing';
import { Subject } from 'rxjs';
import { CadastroPage } from './cadastro.page';
import { CadastroService } from '../services/cadastro.service';
import { CadastroResultado } from '../types/cadastro';
function setup() {
 const result = new Subject<CadastroResultado>(); const solicitar = vi.fn(() => result);
 TestBed.configureTestingModule({providers:[{provide:CadastroService,useValue:{solicitar}}]});
 const page = TestBed.runInInjectionContext(() => new CadastroPage());
 return {page,result,solicitar};
}
afterEach(() => TestBed.resetTestingModule());
it('bloqueia obrigatórios, email inválido e CPF fora do formato', () => {
 const {page,solicitar} = setup();
 for (const value of [{nome:'',email:'',cpf:''},{nome:'   ',email:'ana@example.com',cpf:'12345678901'},{nome:'Ana',email:'invalido',cpf:'12345678901'},{nome:'Ana',email:'ana@example.com',cpf:'123.456.789-01'},{nome:'Ana',email:'ana@example.com',cpf:'123'}]) {
  page.form.setValue(value); page.enviar(); expect(page.form.invalid).toBe(true);
 }
 expect(solicitar).not.toHaveBeenCalled();
});
it('evita envio duplo, mantém dados e libera botão após erro', () => {
 const {page,result,solicitar} = setup();
 page.form.setValue({nome:' Ana ',email:'ana@example.com',cpf:'12345678901'});
 page.enviar(); page.enviar(); expect(solicitar).toHaveBeenCalledTimes(1);
 expect(solicitar.mock.calls[0]).toEqual([{nome:'Ana',email:'ana@example.com',cpf:'12345678901'}]);
 expect(page.enviando()).toBe(true); result.error(new Error());
 expect(page.enviando()).toBe(false); expect(page.erro()).not.toBe(''); expect(page.resultado()).toBeNull();
 expect(page.form.controls.nome.value).toBe(' Ana ');
});
