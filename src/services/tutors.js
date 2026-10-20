import { apiFetch } from './api';

export async function buscarPetsDoTutor(idTutor) {
  const tutorId = String(idTutor);
  const respostaFiltrada = await apiFetch(`/pets?${new URLSearchParams({ tutorId })}`);
  if (!respostaFiltrada.ok) {
    throw new Error('Não foi possível carregar os pets vinculados ao tutor.');
  }

  const petsFiltrados = await respostaFiltrada.json();
  const petsCorrespondentes = petsFiltrados.filter(
    (pet) => String(pet.tutorId) === tutorId,
  );
  if (petsCorrespondentes.length > 0) return petsCorrespondentes;

  const respostaPets = await apiFetch('/pets');
  if (!respostaPets.ok) {
    throw new Error('Não foi possível verificar os pets vinculados ao tutor.');
  }
  const todosOsPets = await respostaPets.json();
  return todosOsPets.filter((pet) => String(pet.tutorId) === tutorId);
}
