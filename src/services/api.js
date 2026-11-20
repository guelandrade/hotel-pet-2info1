const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

export async function apiRequest(path, options = {}) {
  const headers = { ...options.headers };
  if (options.body && !headers['Content-Type']) {
    headers['Content-Type'] = 'application/json';
  }

  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const payload = await response.json();
    const detail =
      typeof payload.detail === 'string'
        ? payload.detail
        : `A API retornou um erro (${response.status}).`;
    throw new Error(detail);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}
