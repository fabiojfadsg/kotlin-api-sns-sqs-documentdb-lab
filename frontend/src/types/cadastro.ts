export interface CadastroRequest { nome: string; email: string; cpf: string; }
export interface CadastroResultado { modo: 'demonstracao' | 'api'; payload: CadastroRequest; }
