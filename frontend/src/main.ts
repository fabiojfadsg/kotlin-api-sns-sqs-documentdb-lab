import { bootstrapApplication } from '@angular/platform-browser';
import { provideHttpClient } from '@angular/common/http';
import { CadastroPage } from './pages/cadastro.page';

bootstrapApplication(CadastroPage, { providers: [provideHttpClient()] }).catch(console.error);
