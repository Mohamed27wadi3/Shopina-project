/**
 * API Client with automatic token refresh handling
 */

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

interface FetchOptions extends RequestInit {
  skipAuth?: boolean;
}

/**
 * Decode JWT token to check expiration
 */
function decodeJWT(token: string): any {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64).split('').map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)).join('')
    );
    return JSON.parse(jsonPayload);
  } catch {
    return null;
  }
}

/**
 * Check if token is expired
 */
function isTokenExpired(token: string): boolean {
  const decoded = decodeJWT(token);
  if (!decoded || !decoded.exp) return true;
  return Date.now() >= decoded.exp * 1000;
}

/**
 * Refresh the access token
 */
async function refreshAccessToken(): Promise<boolean> {
  try {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) return false;

    const response = await fetch(`${API_BASE}/api/users/token/refresh/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh: refreshToken }),
    });

    if (response.ok) {
      const data = await response.json();
      localStorage.setItem('access_token', data.access);
      if (data.refresh) {
        localStorage.setItem('refresh_token', data.refresh);
      }
      console.log('✅ Token refreshed automatically');
      return true;
    }

    // Refresh failed - clear auth
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    return false;
  } catch (error) {
    console.error('❌ Token refresh failed:', error);
    return false;
  }
}

/**
 * Fetch with automatic token refresh
 */
export async function apiFetch(
  endpoint: string,
  options: FetchOptions = {}
): Promise<Response> {
  const { skipAuth = false, ...fetchOptions } = options;

  // Build headers
  const headers = new Headers(fetchOptions.headers || {});

  // Add auth token if needed
  if (!skipAuth) {
    let token = localStorage.getItem('access_token');

    // Check if token is expired and refresh if needed
    if (token && isTokenExpired(token)) {
      console.log('⏰ Token expired - refreshing...');
      const refreshed = await refreshAccessToken();
      if (!refreshed) {
        throw new Error('Session expired. Please login again.');
      }
      token = localStorage.getItem('access_token');
    }

    if (token) {
      headers.set('Authorization', `Bearer ${token}`);
    }
  }

  // Ensure we have content type
  if (!headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json');
  }

  // Make the request
  let response = await fetch(`${API_BASE}${endpoint}`, {
    ...fetchOptions,
    headers,
    credentials: 'include',
  });

  // If we get 401, try to refresh and retry once
  if (response.status === 401 && !skipAuth) {
    console.log('🔄 Got 401 - attempting token refresh');
    const refreshed = await refreshAccessToken();
    if (refreshed) {
      const token = localStorage.getItem('access_token');
      if (token) {
        headers.set('Authorization', `Bearer ${token}`);
        response = await fetch(`${API_BASE}${endpoint}`, {
          ...fetchOptions,
          headers,
          credentials: 'include',
        });
      }
    }
  }

  return response;
}

/**
 * Convenience methods
 */
export async function apiGet(endpoint: string, options?: FetchOptions) {
  return apiFetch(endpoint, { ...options, method: 'GET' });
}

export async function apiPost(endpoint: string, body?: any, options?: FetchOptions) {
  return apiFetch(endpoint, {
    ...options,
    method: 'POST',
    body: body ? JSON.stringify(body) : undefined,
  });
}

export async function apiPut(endpoint: string, body?: any, options?: FetchOptions) {
  return apiFetch(endpoint, {
    ...options,
    method: 'PUT',
    body: body ? JSON.stringify(body) : undefined,
  });
}

export async function apiPatch(endpoint: string, body?: any, options?: FetchOptions) {
  return apiFetch(endpoint, {
    ...options,
    method: 'PATCH',
    body: body ? JSON.stringify(body) : undefined,
  });
}

export async function apiDelete(endpoint: string, options?: FetchOptions) {
  return apiFetch(endpoint, { ...options, method: 'DELETE' });
}

/**
 * Helper to handle API response with proper error handling
 */
export async function apiResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let errorMsg = `API Error: ${response.status}`;
    try {
      const data = await response.json();
      errorMsg = data.detail || data.message || JSON.stringify(data);
    } catch {
      errorMsg = await response.text() || errorMsg;
    }
    throw new Error(errorMsg);
  }
  return response.json();
}
