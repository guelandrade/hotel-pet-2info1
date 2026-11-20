<script setup>
import { onMounted, ref } from 'vue';
import { RouterLink, useRoute, useRouter } from 'vue-router';
import { apiRequest } from '../services/api';

const route = useRoute();
const router = useRouter();
const pet = ref(null);
const tutor = ref(null);
const erro = ref('');
const carregando = ref(true);
const excluindo = ref(false);

async function carregarPet() {
  erro.value = '';
  try {
    pet.value = await apiRequest(`/pets/${route.params.id}`);
    tutor.value = await apiRequest(`/tutores/${pet.value.tutorId}`);
  } catch (error) {
    erro.value =
      error instanceof Error ? error.message : 'Não foi possível carregar o pet.';
  } finally {
    carregando.value = false;
  }
}

async function excluirPet() {
  if (!window.confirm('Deseja realmente excluir este pet?')) {
    return;
  }

  erro.value = '';
  excluindo.value = true;
  try {
    await apiRequest(`/pets/${route.params.id}`, { method: 'DELETE' });
    await router.push({ name: 'pets' });
  } catch (error) {
    erro.value =
      error instanceof Error ? error.message : 'Não foi possível excluir o pet.';
  } finally {
    excluindo.value = false;
  }
}

onMounted(carregarPet);
</script>

<template>
  <section>
    <p v-if="carregando" role="status">Carregando detalhes do pet...</p>
    <p v-else-if="erro && !pet" class="alert alert-danger" role="alert">
      {{ erro }}
    </p>

    <template v-else-if="pet">
      <p v-if="erro" class="alert alert-danger" role="alert">{{ erro }}</p>

      <RouterLink
        class="link-success fw-semibold text-decoration-none"
        :to="{ name: 'pets' }"
      >
        Voltar para pets
      </RouterLink>

      <header class="mt-4 mb-4">
        <h1 class="display-6 fw-bold mb-2">{{ pet.nome }}</h1>
        <p class="text-body-secondary mb-0">Identificador: {{ pet.id }}</p>
      </header>

      <dl class="row g-4">
        <div class="col-sm-6">
          <dt class="text-body-secondary small mb-2">Espécie</dt>
          <dd class="fs-5">{{ pet.especie }}</dd>
        </div>
        <div class="col-sm-6">
          <dt class="text-body-secondary small mb-2">Tutor</dt>
          <dd class="fs-5">{{ tutor?.nome ?? 'Tutor não encontrado' }}</dd>
          <dd>{{ tutor?.telefone }}</dd>
        </div>
      </dl>

      <button
        class="btn btn-danger"
        type="button"
        :disabled="excluindo"
        @click="excluirPet"
      >
        {{ excluindo ? 'Excluindo...' : 'Excluir pet' }}
      </button>
    </template>
  </section>
</template>
