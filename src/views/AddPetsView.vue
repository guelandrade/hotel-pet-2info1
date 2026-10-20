<script setup>
import { onMounted, reactive, ref } from 'vue';
import { RouterLink, useRouter } from 'vue-router';
import { apiFetch } from '@/services/api';

const novoPet = reactive({
  nome: '',
  especie: '',
  tutorId: '',
});
const tutores = ref([]);
const carregandoTutores = ref(true);
const salvando = ref(false);
const erro = ref('');
const router = useRouter();

async function carregarTutores() {
  carregandoTutores.value = true;
  erro.value = '';
  try {
    const resposta = await apiFetch('/tutores');
    if (!resposta.ok) {
      throw new Error('Não foi possível carregar os tutores.');
    }
    tutores.value = await resposta.json();
  } catch (error) {
    erro.value = error instanceof Error
      ? error.message
      : 'Não foi possível carregar os tutores.';
  } finally {
    carregandoTutores.value = false;
  }
}

async function salvarPet() {
  if (!novoPet.nome.trim() || !novoPet.especie || !novoPet.tutorId) return;

  salvando.value = true;
  erro.value = '';
  try {
    const resposta = await apiFetch('/pets', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        nome: novoPet.nome.trim(),
        especie: novoPet.especie,
        tutorId: novoPet.tutorId,
      }),
    });
    if (!resposta.ok) {
      throw new Error('Não foi possível cadastrar o pet. Tente novamente.');
    }
    await router.push({ name: 'pets' });
  } catch (error) {
    erro.value = error instanceof Error
      ? error.message
      : 'Não foi possível cadastrar o pet. Tente novamente.';
  } finally {
    salvando.value = false;
  }
}

onMounted(carregarTutores);
</script>

<template>
  <div class="container-fluid">
    <header class="mb-4">
      <h1 class="h2 mb-1">Cadastrar Pet</h1>
      <p class="text-body-secondary mb-0">Preencha os dados para cadastrar um novo pet.</p>
    </header>

    <div v-if="erro" class="alert alert-danger" role="alert">{{ erro }}</div>
    <p v-if="carregandoTutores" class="text-body-secondary" role="status">
      Carregando tutores...
    </p>
    <form v-else class="row g-3" @submit.prevent="salvarPet">
      <div class="col-12 col-md-6">
        <label for="nome-pet" class="form-label">Nome do Pet</label>
        <input
          id="nome-pet"
          v-model.trim="novoPet.nome"
          class="form-control"
          type="text"
          placeholder="Digite o nome do pet"
          required
        />
      </div>

      <div class="col-12 col-md-6">
        <label for="especie-pet" class="form-label">Espécie</label>
        <select
          id="especie-pet"
          v-model="novoPet.especie"
          class="form-select"
          required
        >
          <option value="" disabled>Selecione a espécie</option>
          <option value="Cachorro">Cachorro</option>
          <option value="Gato">Gato</option>
        </select>
      </div>

      <div class="col-12 col-md-6">
        <label for="tutor-pet" class="form-label">Tutor</label>
        <select
          id="tutor-pet"
          v-model="novoPet.tutorId"
          class="form-select"
          required
        >
          <option value="" disabled>Selecione o tutor</option>
          <option v-for="tutor in tutores" :key="tutor.id" :value="tutor.id">
            {{ tutor.nome }}
          </option>
        </select>
      </div>

      <div class="col-12 d-flex justify-content-end gap-2">
        <RouterLink class="btn btn-outline-secondary" :to="{ name: 'pets' }">
          Cancelar
        </RouterLink>
        <button
          class="btn btn-primary"
          type="submit"
          :disabled="!novoPet.nome || !novoPet.especie || !novoPet.tutorId || salvando"
        >
          {{ salvando ? 'Cadastrando...' : 'Cadastrar Pet' }}
        </button>
      </div>
    </form>
  </div>
</template>
