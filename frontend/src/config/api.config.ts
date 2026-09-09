import { InjectionToken } from '@angular/core';

export interface ApiConfig { demo: boolean; baseUrl: string; }
// Configuração pública compilada no frontend. Nunca incluir segredos.
export const apiConfig: ApiConfig = { demo: true, baseUrl: 'http://localhost:8080' };
export const API_CONFIG = new InjectionToken<ApiConfig>('API_CONFIG', { providedIn: 'root', factory: () => apiConfig });
