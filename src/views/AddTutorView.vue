<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { apiRequest } from '../services/api';

const novoTutor = ref({
  nome: '',
  telefone: '',
});

const router = useRouter();
const erro = ref('');
const salvando = ref(false);

async function salvarTutor() {
  erro.value = '';
  salvando.value = true;
  try {
    await apiRequest('/tutores', {
      method: 'POST',
      body: JSON.stringify(novoTutor.value),
    });
    await router.push('/tutores');
  } catch (error) {
    erro.value =
      error instanceof Error ? error.message : 'Não foi possível cadastrar o tutor.';
  } finally {
    salvando.value = false;
  }
}
</script>

<template>
  <div>
    <header class="mb-4">
      <h1 class="text-2xl font-bold">Cadastrar Tutor</h1>
      <p class="text-body-secondary mb-0">Cadastro de tutores no sistema.</p>
    </header>

    <p v-if="erro" class="alert alert-danger" role="alert">{{ erro }}</p>

    <form @submit.prevent="salvarTutor">
      <div class="col-md-6">
        <label
          for="nome"
          class="form-label"
        >
          Nome do Tutor
        </label>

        <input
          type="text"
          id="nome"
          v-model="novoTutor.nome"
          class="form-control"
          required
        />
      </div>

      <div class="col-md-6 mt-3">
        <label for="telefone" class="form-label">Telefone</label>
        <input
          id="telefone"
          v-model="novoTutor.telefone"
          type="tel"
          class="form-control"
          required
        />
      </div>

      <button class="btn btn-primary mt-3" type="submit" :disabled="salvando">
        {{ salvando ? 'Salvando...' : 'Salvar Tutor' }}
      </button>
    </form>
  </div>
</template>
