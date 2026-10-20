<script setup>
import { onMounted, ref } from 'vue';
import { RouterLink, useRoute } from 'vue-router';
import { apiFetch } from '@/services/api';

const route = useRoute();
const pet = ref(null);
const tutor = ref(null);
const carregando = ref(true);
const erro = ref('');

async function carregarPet() {
  carregando.value = true;
  erro.value = '';
  try {
    const respostaPet = await apiFetch(`/pets/${encodeURIComponent(route.params.id)}`);
    if (!respostaPet.ok) {
      throw new Error(
        respostaPet.status === 404
          ? 'Pet não encontrado.'
          : 'Não foi possível carregar os dados do pet.',
      );
    }
    pet.value = await respostaPet.json();

    if (pet.value.tutorId) {
      const respostaTutor = await apiFetch(
        `/tutores/${encodeURIComponent(pet.value.tutorId)}`,
      );
      if (respostaTutor.ok) {
        tutor.value = await respostaTutor.json();
      }
    }
  } catch (error) {
    erro.value = error instanceof Error
      ? error.message
      : 'Não foi possível carregar os dados do pet.';
  } finally {
    carregando.value = false;
  }
}

onMounted(carregarPet);
</script>

<template>
  <div class="container-fluid">
    <header class="d-flex flex-wrap align-items-center justify-content-between gap-3 mb-4">
      <h1 class="h2 mb-0">Detalhes do Pet</h1>
      <RouterLink class="btn btn-outline-primary" :to="{ name: 'pets' }">
        <i class="bi bi-arrow-left me-2" aria-hidden="true"></i>
        Voltar para Pets
      </RouterLink>
    </header>

    <div v-if="erro" class="alert alert-danger" role="alert">{{ erro }}</div>
    <p v-if="carregando" class="text-body-secondary py-3" role="status">
      Carregando dados do pet...
    </p>
    <section v-else-if="pet" class="card shadow-sm">
      <div class="card-header bg-white">
        <h2 class="h5 mb-0">{{ pet.nome }}</h2>
      </div>
      <div class="card-body">
        <dl class="row mb-0">
          <div class="col-12 col-md-4">
            <dt>ID</dt>
            <dd>{{ pet.id }}</dd>
          </div>
          <div class="col-12 col-md-4">
            <dt>Espécie</dt>
            <dd>{{ pet.especie }}</dd>
          </div>
          <div class="col-12 col-md-4">
            <dt>Tutor</dt>
            <dd>{{ tutor?.nome || 'Tutor não encontrado' }}</dd>
          </div>
        </dl>
      </div>
    </section>
  </div>
</template>
