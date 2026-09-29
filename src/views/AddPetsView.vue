<script setup>
import { onMounted, ref } from 'vue';
import { RouterLink, useRouter } from 'vue-router';

onMounted();

const novoPet = ref({
  nome: '',
  especie: '',
  tutorId: '',
});

const API_URL = 'http://localhost:3000/pets';
const tutores = ref([]);
const router = useRouter();

async function carregarTutores() {
  const resposta = await fetch(`${API_URL}/tutores`);
  console.log('load tutores', tutores);
  tutores.value = await resposta.json();
}

async function salvarPet() {
  const resposta = await fetch(`${API_URL}/pets`, {
    method: 'POST',
    headers: {
      'Content-type': 'application/json',
    },
    body: JSON.stringify(novoPet.value),
  });
  router.push('/pets');
}
</script>

<template>
  <div>
    <header class="mb-4">
      <h1 class="text-2xl font-bold">Listagem de Pets</h1>
      <p class="text-body-secondary mb-0">Cadastro de Pets no sistema.</p>
    </header>

    <RouterLink
      class="btn btn-primary"
      :to="{ name: 'addPet' }"
    >
      Adicionar Pet
    </RouterLink>

    <form @submit.prevent="salvarPet">
      <div class="col-md-6">
        <label
          for="nome"
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
          for="especie"
          class="form-label"
        >
          Espécies
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
            Selecionar a espécie
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
            Selecionar o tutor
          </option>
          <option
            v-for="tutor in tutores"
            :key="tutor.id"
            :value="tutor.id"
          >
            {{ tutor.nome }}
          </option>
        </select>
      </div>
    </form>
  </div>
</template>
