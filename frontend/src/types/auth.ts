export type Role =
  | 'admin_systeme'
  | 'accueil'
  | 'medecin'
  | 'infirmier'
  | 'pharmacien'
  | 'directeur';

export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: Role;
  is_active: boolean;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface TokenPair {
  access: string;
  refresh: string;
}

export interface LoginResponse {
  user: User;
  tokens: TokenPair;
}
