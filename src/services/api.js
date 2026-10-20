export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000';

export async function apiFetch(path, options) {
  try {
    return await fetch(`${API_URL}${path}`, options);
  } catch (error) {
    if (error instanceof TypeError) {
      throw new Error(
        'Não foi possível conectar à API. Execute "npm run dev" para iniciar a aplicação e o servidor.',
        { cause: error },
      );
    }
    throw error;
  }
}
