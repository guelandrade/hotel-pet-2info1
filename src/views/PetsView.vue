<script setup>
import { onMounted, ref } from 'vue';
import { RouterLink } from 'vue-router';
import { apiRequest } from '../services/api';

const pets = ref([]);
const tutores = ref([]);
const loading = ref(true);
const erro = ref('');
const especieFiltro = ref('');

async function carregarDados() {
  erro.value = '';
  loading.value = true;
  try {
    const filtro =
      especieFiltro.value === ''
        ? ''
        : `?especie=${encodeURIComponent(especieFiltro.value)}`;
    [pets.value, tutores.value] = await Promise.all([
      apiRequest(`/pets${filtro}`),
      apiRequest('/tutores'),
    ]);
  } catch (error) {
    erro.value =
      error instanceof Error ? error.message : 'Não foi possível carregar os pets.';
  } finally {
    loading.value = false;
  }
}

function nomeDoTutor(tutorId) {
  return (
    tutores.value.find((tutor) => tutor.id === tutorId)?.nome ??
    'Tutor não encontrado'
  );
}

async function excluirPet(id) {
  if (!window.confirm('Deseja realmente excluir este pet?')) {
    return;
  }

  try {
    await apiRequest(`/pets/${id}`, { method: 'DELETE' });
    await carregarDados();
  } catch (error) {
    erro.value =
      error instanceof Error ? error.message : 'Não foi possível excluir o pet.';
  }
}

onMounted(carregarDados);
</script>

<template>
  <div>
    <header class="mb-4">
      <h1 class="text-2xl font-bold">Listagem de Pets</h1>
      <p class="text-body-secondary mb-0">
        Listagem dos Pets cadastrados no sistema.
      </p>
    </header>

    <p v-if="loading" role="status">Carregando pets...</p>
    <p v-if="erro" class="alert alert-danger" role="alert">{{ erro }}</p>

    <RouterLink
      class="btn btn-primary"
      :to="{ name: 'addPet' }"
    >
      Adicionar Pet
    </RouterLink>

    <div class="my-3">
      <label for="filtro-especie" class="form-label">Filtrar por espécie</label>
      <select
        id="filtro-especie"
        v-model="especieFiltro"
        class="form-select"
        @change="carregarDados"
      >
        <option value="">Todas</option>
        <option value="Cachorro">Cachorro</option>
        <option value="Gato">Gato</option>
      </select>
    </div>

    <table v-if="!loading" class="table table-striped table-hover">
      <thead>
        <tr>
          <th>ID</th>
          <th>Nome</th>
          <th>Espécie</th>
          <th>Tutor</th>
          <th>Ações</th>
        </tr>
      </thead>

      <tbody>
        <tr
          v-for="pet in pets"
          :key="pet.id"
        >
          <td>{{ pet.id }}</td>
          <td>{{ pet.nome }}</td>
          <td>{{ pet.especie }}</td>
          <td>{{ nomeDoTutor(pet.tutorId) }}</td>
          <td>
            <RouterLink :to="`/pets/${pet.id}`"> Visualizar </RouterLink>
            <button class="btn btn-danger mr-5" @click="excluirPet(pet.id)">
              Excluir
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
