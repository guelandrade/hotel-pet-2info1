<script setup>
import { onMounted, ref } from 'vue';
import { RouterLink, useRoute } from 'vue-router';
import { apiRequest } from '../services/api';

const route = useRoute();
const tutor = ref(null);
const pets = ref([]);
const erro = ref('');
const carregando = ref(true);

async function carregarTutor() {
  try {
    const [dadosTutor, todosPets] = await Promise.all([
      apiRequest(`/tutores/${route.params.id}`),
      apiRequest('/pets'),
    ]);
    tutor.value = dadosTutor;
    pets.value = todosPets.filter((pet) => pet.tutorId === dadosTutor.id);
  } catch (error) {
    erro.value =
      error instanceof Error ? error.message : 'Não foi possível carregar o tutor.';
  } finally {
    carregando.value = false;
  }
}

onMounted(carregarTutor);
</script>

<template>
  <section>
    <p v-if="carregando" role="status">Carregando detalhes do tutor...</p>
    <p v-else-if="erro" class="alert alert-danger" role="alert">{{ erro }}</p>

    <template v-else-if="tutor">
      <RouterLink
        class="link-success fw-semibold text-decoration-none"
        :to="{ name: 'tutores' }"
      >
        Voltar para tutores
      </RouterLink>

      <header class="mt-4 mb-4">
        <h1 class="display-6 fw-bold mb-2">{{ tutor.nome }}</h1>
        <p class="text-body-secondary mb-0">Identificador: {{ tutor.id }}</p>
      </header>

      <h2 class="h5">Telefone</h2>
      <p>{{ tutor.telefone }}</p>

      <h2 class="h5 mt-4">Pets</h2>
      <p v-if="pets.length === 0">Este tutor ainda não possui pets.</p>
      <ul v-else>
        <li v-for="pet in pets" :key="pet.id">
          <RouterLink :to="`/pets/${pet.id}`">
            {{ pet.nome }} ({{ pet.especie }})
          </RouterLink>
        </li>
      </ul>
    </template>
  </section>
</template>
