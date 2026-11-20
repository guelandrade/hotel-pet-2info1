<script setup>
import { onMounted, ref } from 'vue';
import { RouterLink } from 'vue-router';
import { apiRequest } from '../services/api';

const tutores = ref([]);
const loading = ref(true);
const erro = ref('');

async function carregarDados() {
  erro.value = '';
  loading.value = true;
  try {
    tutores.value = await apiRequest('/tutores');
  } catch (error) {
    erro.value =
      error instanceof Error ? error.message : 'Não foi possível carregar os tutores.';
  } finally {
    loading.value = false;
  }
}

async function excluirTutor(id) {
  if (!window.confirm('Deseja realmente excluir este tutor?')) {
    return;
  }

  try {
    await apiRequest(`/tutores/${id}`, { method: 'DELETE' });
    await carregarDados();
  } catch (error) {
    erro.value =
      error instanceof Error ? error.message : 'Não foi possível excluir o tutor.';
  }
}

onMounted(carregarDados);
</script>

<template>
  <div>
    <header class="mb-4">
      <h1 class="text-2xl font-bold">Listagem de Tutores</h1>
      <p class="text-body-secondary mb-0">
        Listagem dos Tutores cadastrados no sistema.
      </p>
    </header>

    <p v-if="loading" role="status">Carregando tutores...</p>
    <p v-if="erro" class="alert alert-danger" role="alert">{{ erro }}</p>

    <RouterLink
      class="btn btn-primary"
      :to="{ name: 'addTutor' }"
    >
      Adicionar Tutor
    </RouterLink>

    <table v-if="!loading" class="table table-striped table-hover">
      <thead>
        <tr>
          <th>ID</th>
          <th>Nome</th>
          <th>Telefone</th>
          <th>Ações</th>
        </tr>
      </thead>

      <tbody>
        <tr
          v-for="tutor in tutores"
          :key="tutor.id"
        >
          <td>{{ tutor.id }}</td>
          <td>{{ tutor.nome }}</td>
          <td>{{ tutor.telefone }}</td>
          <td>
            <RouterLink :to="`/tutores/${tutor.id}`"> Visualizar </RouterLink>
            <button class="btn btn-danger mr-5" @click="excluirTutor(tutor.id)">
              Excluir
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
