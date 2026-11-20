export const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

export async function apiFetch(path, options = {}) {
  try {
    return await fetch(`${API_URL}${path}`, options);
  } catch (error) {
    if (error instanceof TypeError) {
      throw new Error(
        'Não foi possível conectar à API FastAPI. Verifique se o servidor está em execução.',
        { cause: error },
      );
    }
    throw error;
  }
}
