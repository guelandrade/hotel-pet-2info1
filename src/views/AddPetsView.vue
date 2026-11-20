<script setup>
import { onMounted, ref } from 'vue';
import { RouterLink, useRouter } from 'vue-router';
import { apiRequest } from '../services/api';

const novoPet = ref({
  nome: '',
  especie: '',
  tutorId: '',
});

const router = useRouter();
const tutores = ref([]);
const carregandoTutores = ref(true);
const erro = ref('');
const salvando = ref(false);

async function carregarTutores() {
  erro.value = '';
  try {
    tutores.value = await apiRequest('/tutores');
  } catch (error) {
    erro.value =
      error instanceof Error ? error.message : 'Não foi possível carregar os tutores.';
  } finally {
    carregandoTutores.value = false;
  }
}

async function salvarPet() {
  erro.value = '';
  salvando.value = true;
  try {
    await apiRequest('/pets', {
      method: 'POST',
      body: JSON.stringify(novoPet.value),
    });
    await router.push('/pets');
  } catch (error) {
    erro.value =
      error instanceof Error ? error.message : 'Não foi possível cadastrar o pet.';
  } finally {
    salvando.value = false;
  }
}

onMounted(carregarTutores);
</script>

<template>
  <div>
    <header class="mb-4">
      <h1 class="text-2xl font-bold">Cadastrar Pet</h1>
      <p class="text-body-secondary mb-0">Cadastro de Pets no sistema.</p>
    </header>

    <RouterLink
      class="btn btn-outline-secondary mb-3"
      :to="{ name: 'pets' }"
    >
      Voltar para pets
    </RouterLink>

    <p v-if="carregandoTutores" role="status">Carregando tutores...</p>
    <p v-if="erro" class="alert alert-danger" role="alert">{{ erro }}</p>

    <form v-if="!carregandoTutores" @submit.prevent="salvarPet">
      <div class="col-md-6">
        <label
          for="especie"
          class="form-label"
        >
          Nome do Pet
        </label>

        <input
          type="text"
          id="nome"
          v-model="novoPet.nome"
          class="form-control"
          required
        />
      </div>

      <div class="col-md-6">
        <label
          for="nome"
          class="form-label"
        >
          Espécie
        </label>

        <select
          id="especie"
          v-model="novoPet.especie"
          class="form-select"
          required
        >
          <option
            value=""
            disabled
          >
            Selecione a Espécie
          </option>
          <option value="Cachorro">Cachorro</option>
          <option value="Gato">Gato</option>
        </select>
      </div>

      <div class="col-md-6">
        <label
          for="tutor"
          class="form-label"
        >
          Tutor
        </label>

        <select
          id="tutor"
          v-model="novoPet.tutorId"
          class="form-select"
          required
        >
          <option
            value=""
            disabled
          >
            Selecione um Tutor
          </option>
          <option
            v-for="tutor in tutores"
            :key="tutor.id"
            :value="Number(tutor.id)"
          >
            {{ tutor.nome }}
          </option>
        </select>
      </div>

      <button class="btn btn-primary mt-3" type="submit" :disabled="salvando">
        {{ salvando ? 'Salvando...' : 'Salvar Pet' }}
      </button>
    </form>
  </div>
</template>
