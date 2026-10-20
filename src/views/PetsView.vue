<script setup>
import { onMounted, ref } from 'vue';
import { RouterLink } from 'vue-router';
import { apiFetch } from '@/services/api';

const pets = ref([]);
const tutores = ref([]);
const carregando = ref(true);
const excluindoId = ref('');
const erro = ref('');

async function carregarDados() {
  carregando.value = true;
  erro.value = '';
  try {
    const [respostaPets, respostaTutores] = await Promise.all([
      apiFetch('/pets'),
      apiFetch('/tutores'),
    ]);
    if (!respostaPets.ok || !respostaTutores.ok) {
      throw new Error('Não foi possível carregar os pets e tutores.');
    }
    [pets.value, tutores.value] = await Promise.all([
      respostaPets.json(),
      respostaTutores.json(),
    ]);
  } catch (error) {
    erro.value = error instanceof Error
      ? error.message
      : 'Não foi possível carregar os pets e tutores.';
  } finally {
    carregando.value = false;
  }
}

function nomeDoTutor(tutorId) {
  return tutores.value.find((tutor) => String(tutor.id) === String(tutorId))?.nome
    ?? 'Tutor não encontrado';
}

async function excluirPet(pet) {
  if (!window.confirm(`Deseja realmente excluir o pet ${pet.nome}?`)) return;

  excluindoId.value = String(pet.id);
  erro.value = '';
  try {
    const resposta = await apiFetch(`/pets/${encodeURIComponent(pet.id)}`, {
      method: 'DELETE',
    });
    if (!resposta.ok) {
      throw new Error('Não foi possível excluir o pet. Tente novamente.');
    }
    await carregarDados();
  } catch (error) {
    erro.value = error instanceof Error
      ? error.message
      : 'Não foi possível excluir o pet. Tente novamente.';
  } finally {
    excluindoId.value = '';
  }
}

onMounted(carregarDados);
</script>

<template>
  <div class="container-fluid">
    <header class="d-flex flex-wrap align-items-center justify-content-between gap-3 mb-4">
      <div>
        <h1 class="h2 mb-1">Listagem de Pets</h1>
        <p class="text-body-secondary mb-0">Consulte os pets cadastrados e seus tutores.</p>
      </div>
      <RouterLink class="btn btn-primary" :to="{ name: 'addPet' }">
        <i class="bi bi-plus-lg me-2" aria-hidden="true"></i>
        Cadastrar Pet
      </RouterLink>
    </header>

    <div v-if="erro" class="alert alert-danger" role="alert">{{ erro }}</div>
    <p v-if="carregando" class="text-body-secondary py-3" role="status">
      Carregando pets...
    </p>
    <div v-else class="table-responsive">
      <table class="table table-striped table-hover align-middle">
        <thead class="table-light">
          <tr>
            <th scope="col">ID</th>
            <th scope="col">Nome</th>
            <th scope="col">Espécie</th>
            <th scope="col">Tutor</th>
            <th scope="col">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="pet in pets" :key="pet.id">
            <td>{{ pet.id }}</td>
            <td>{{ pet.nome }}</td>
            <td>{{ pet.especie }}</td>
            <td>{{ nomeDoTutor(pet.tutorId) }}</td>
            <td>
              <div class="d-flex flex-wrap gap-2">
                <RouterLink
                  class="btn btn-sm btn-outline-primary"
                  :to="{ name: 'detalhes-pet', params: { id: pet.id } }"
                >
                  Visualizar
                </RouterLink>
                <button
                  class="btn btn-sm btn-outline-danger"
                  type="button"
                  :disabled="excluindoId === String(pet.id)"
                  @click="excluirPet(pet)"
                >
                  {{ excluindoId === String(pet.id) ? 'Excluindo...' : 'Excluir' }}
                </button>
              </div>
            </td>
          </tr>
          <tr v-if="pets.length === 0">
            <td colspan="5" class="text-center text-body-secondary py-4">
              Nenhum pet cadastrado.
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
