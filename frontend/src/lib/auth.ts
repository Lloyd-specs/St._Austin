export function setTokens(access: string, refresh: string): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem('access_token', access);
  localStorage.setItem('refresh_token', refresh);
}

export function getAccessToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('access_token');
}

export function getRefreshToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('refresh_token');
}

export function clearTokens(): void {
  if (typeof window === 'undefined') return;
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
}

interface JWTPayload {
  user_id: string;
  email: string;
  full_name: string;
  role: string;
  preferred_language: string;
  exp: number;
  iat: number;
  [key: string]: unknown;
}

export function getUserFromToken(): JWTPayload | null {
  const token = getAccessToken();
  if (!token) return null;

  try {
    const parts = token.split('.');
    if (parts.length !== 3) return null;

    const payload = parts[1];
    // Base64url decode
    const base64 = payload.replace(/-/g, '+').replace(/_/g, '/');
    const jsonStr = atob(base64);
    const decoded = JSON.parse(jsonStr) as JWTPayload;

    // Check expiration
    if (decoded.exp && decoded.exp * 1000 < Date.now()) {
      clearTokens();
      return null;
    }

    return decoded;
  } catch {
    return null;
  }
}
