<script setup>
import { computed, onMounted, ref } from 'vue';
import { RouterLink } from 'vue-router';
import { apiFetch } from '@/services/api';
import { buscarPetsDoTutor } from '@/services/tutors';

const tutores = ref([]);
const pets = ref([]);
const carregando = ref(true);
const removendoId = ref('');
const busca = ref('');
const erro = ref('');

function normalizarBusca(valor) {
  return String(valor)
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLocaleLowerCase('pt-BR')
    .replace(/[^\p{L}\p{N}]/gu, '');
}

const tutoresFiltrados = computed(() => {
  const termo = normalizarBusca(busca.value.trim());
  if (!termo) return tutores.value;

  return tutores.value.filter((tutor) => {
    const campos = [tutor.nome, tutor.cpfCnpj, tutor.email].filter(Boolean);
    return campos.some((valor) => normalizarBusca(valor).includes(termo));
  });
});

async function carregarDados() {
  carregando.value = true;
  erro.value = '';
  try {
    const [respostaTutores, respostaPets] = await Promise.all([
      apiFetch('/tutores'),
      apiFetch('/pets'),
    ]);
    if (!respostaTutores.ok || !respostaPets.ok) {
      throw new Error('Não foi possível carregar os tutores e pets.');
    }
    [tutores.value, pets.value] = await Promise.all([
      respostaTutores.json(),
      respostaPets.json(),
    ]);
  } catch (error) {
    erro.value = error instanceof Error
      ? error.message
      : 'Não foi possível carregar os tutores e pets.';
  } finally {
    carregando.value = false;
  }
}

function petsDoTutor(tutor) {
  return pets.value.filter((pet) => String(pet.tutorId) === String(tutor.id));
}

function documentoMascarado(tutor) {
  const digitos = String(tutor.cpfCnpj ?? '').replace(/\D/g, '');
  if (digitos.length === 11) return '***.***.***-**';
  if (digitos.length === 14) return '**.***.***/****-**';
  return tutor.cpfCnpj ? '***' : '—';
}

async function excluirTutor(tutor) {
  if (!window.confirm(`Deseja realmente excluir o tutor ${tutor.nome}?`)) return;

  removendoId.value = String(tutor.id);
  erro.value = '';
  try {
    const petsVinculados = await buscarPetsDoTutor(tutor.id);
    if (petsVinculados.length > 0) {
      window.alert('Este tutor possui pets vinculados. Remova ou transfira os pets antes de excluir o tutor.');
      return;
    }

    const resposta = await apiFetch(`/tutores/${encodeURIComponent(tutor.id)}`, {
      method: 'DELETE',
    });
    if (!resposta.ok) {
      throw new Error('Não foi possível remover o tutor. Tente novamente.');
    }
    await carregarDados();
  } catch (error) {
    erro.value = error instanceof Error
      ? error.message
      : 'Não foi possível remover o tutor. Tente novamente.';
  } finally {
    removendoId.value = '';
  }
}

onMounted(carregarDados);
</script>

<template>
  <div class="container-fluid">
    <header class="d-flex flex-wrap align-items-start justify-content-between gap-3 mb-4">
      <div>
        <h1 class="h2 mb-1">Listagem de Tutores</h1>
        <p class="text-body-secondary mb-0">Consulte os tutores cadastrados e seus pets.</p>
      </div>
      <RouterLink class="btn btn-primary" :to="{ name: 'addTutor' }">
        <i class="bi bi-plus-lg me-2" aria-hidden="true"></i>
        Cadastrar Tutor
      </RouterLink>
    </header>

    <div class="row mb-3">
      <div class="col-12 col-lg-8">
        <label class="visually-hidden" for="buscar-tutor">Pesquisar tutores</label>
        <div class="input-group">
          <span class="input-group-text bg-white" aria-hidden="true">
            <i class="bi bi-search"></i>
          </span>
          <input
            id="buscar-tutor"
            v-model="busca"
            class="form-control"
            type="search"
            placeholder="Pesquisar tutor por nome, CPF/CNPJ ou e-mail"
          />
        </div>
      </div>
    </div>

    <div v-if="erro" class="alert alert-danger" role="alert">{{ erro }}</div>
    <div v-if="carregando" class="text-body-secondary py-3" role="status">
      Carregando tutores...
    </div>
    <div v-else class="table-responsive">
      <table class="table table-bordered table-striped table-hover align-middle">
        <thead class="table-light">
          <tr>
            <th scope="col">ID</th>
            <th scope="col">Nome Completo</th>
            <th scope="col">CPF / CNPJ</th>
            <th scope="col">Telefone / Celular / WhatsApp</th>
            <th scope="col">E-mail</th>
            <th scope="col">Pets (Quantidade)</th>
            <th scope="col">Nomes dos Pets</th>
            <th scope="col">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="tutor in tutoresFiltrados" :key="tutor.id">
            <td>{{ tutor.id }}</td>
            <td>{{ tutor.nome }}</td>
            <td>{{ documentoMascarado(tutor) }}</td>
            <td>{{ tutor.telefone || '—' }}</td>
            <td>{{ tutor.email || '—' }}</td>
            <td class="text-center">{{ petsDoTutor(tutor).length }}</td>
            <td>
              {{ petsDoTutor(tutor).length
                ? petsDoTutor(tutor).map((pet) => pet.nome).join(' / ')
                : 'Nenhum pet vinculado' }}
            </td>
            <td>
              <div class="d-flex flex-wrap gap-2">
                <RouterLink
                  class="btn btn-sm btn-outline-primary"
                  :to="{ name: 'detalhes-tutor', params: { id: tutor.id } }"
                >
                  <i class="bi bi-eye me-1" aria-hidden="true"></i>
                  Visualizar
                </RouterLink>
                <button
                  class="btn btn-sm btn-outline-danger"
                  type="button"
                  :disabled="removendoId === String(tutor.id)"
                  @click="excluirTutor(tutor)"
                >
                  <i class="bi bi-trash me-1" aria-hidden="true"></i>
                  {{ removendoId === String(tutor.id) ? 'Removendo...' : 'Remover' }}
                </button>
              </div>
            </td>
          </tr>
          <tr v-if="tutoresFiltrados.length === 0">
            <td colspan="8" class="text-center text-body-secondary py-4">
              {{ tutores.length ? 'Nenhum tutor encontrado para a pesquisa.' : 'Nenhum tutor cadastrado.' }}
            </td>
          </tr>
        </tbody>
      </table>
      <p class="text-body-secondary border-top pt-3">
        Exibindo {{ tutoresFiltrados.length }}
        {{ tutoresFiltrados.length === 1 ? 'tutor' : 'tutores' }}
      </p>
    </div>
  </div>
</template>
