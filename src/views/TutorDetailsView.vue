<script setup>
import { computed, onMounted, reactive, ref } from 'vue';
import { RouterLink, useRoute, useRouter } from 'vue-router';
import { apiFetch } from '@/services/api';
import { buscarPetsDoTutor } from '@/services/tutors';

const route = useRoute();
const router = useRouter();
const tutor = ref(null);
const pets = ref([]);
const carregando = ref(true);
const cadastrandoPet = ref(false);
const removendoTutor = ref(false);
const erro = ref('');
const novoPet = reactive({ nome: '', especie: '' });

const formularioPetValido = computed(
  () => Boolean(novoPet.nome.trim()) && Boolean(novoPet.especie),
);

function valorOuTraco(valor) {
  return valor || '—';
}

function documentoMascarado(valor) {
  const digitos = String(valor ?? '').replace(/\D/g, '');
  if (digitos.length === 11) return '***.***.***-**';
  if (digitos.length === 14) return '**.***.***/****-**';
  return valor ? '***' : '—';
}

function dataFormatada(valor) {
  if (!valor) return '—';
  const dataIso = String(valor).match(/^(\d{4})-(\d{2})-(\d{2})/);
  if (dataIso) return `${dataIso[3]}/${dataIso[2]}/${dataIso[1]}`;
  return valor;
}

async function carregarDados() {
  carregando.value = true;
  erro.value = '';
  try {
    const idTutor = String(route.params.id);
    const [respostaTutor, respostaPets] = await Promise.all([
      apiFetch(`/tutores/${encodeURIComponent(idTutor)}`),
      buscarPetsDoTutor(idTutor),
    ]);
    if (!respostaTutor.ok) {
      throw new Error(
        respostaTutor.status === 404
          ? 'Tutor não encontrado.'
          : 'Não foi possível carregar os dados do tutor.',
      );
    }
    tutor.value = await respostaTutor.json();
    pets.value = respostaPets;
  } catch (error) {
    erro.value = error instanceof Error
      ? error.message
      : 'Não foi possível carregar os dados do tutor.';
  } finally {
    carregando.value = false;
  }
}

async function cadastrarPet() {
  if (!formularioPetValido.value) return;

  cadastrandoPet.value = true;
  erro.value = '';
  try {
    const resposta = await apiFetch('/pets', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        nome: novoPet.nome.trim(),
        especie: novoPet.especie,
        tutorId: String(route.params.id),
      }),
    });
    if (!resposta.ok) {
      throw new Error('Não foi possível cadastrar o pet. Tente novamente.');
    }
    novoPet.nome = '';
    novoPet.especie = '';
    await carregarDados();
  } catch (error) {
    erro.value = error instanceof Error
      ? error.message
      : 'Não foi possível cadastrar o pet. Tente novamente.';
  } finally {
    cadastrandoPet.value = false;
  }
}

async function excluirTutor() {
  if (!window.confirm(`Deseja realmente excluir o tutor ${tutor.value.nome}?`)) return;

  removendoTutor.value = true;
  erro.value = '';
  try {
    const petsVinculados = await buscarPetsDoTutor(route.params.id);
    if (petsVinculados.length > 0) {
      window.alert('Este tutor possui pets vinculados. Remova ou transfira os pets antes de excluir o tutor.');
      return;
    }

    const resposta = await apiFetch(`/tutores/${encodeURIComponent(route.params.id)}`, {
      method: 'DELETE',
    });
    if (!resposta.ok) {
      throw new Error('Não foi possível remover o tutor. Tente novamente.');
    }
    await router.push({ name: 'tutores' });
  } catch (error) {
    erro.value = error instanceof Error
      ? error.message
      : 'Não foi possível remover o tutor. Tente novamente.';
  } finally {
    removendoTutor.value = false;
  }
}

onMounted(carregarDados);
</script>

<template>
  <div class="container-fluid">
    <header class="d-flex flex-wrap align-items-start justify-content-between gap-3 mb-4">
      <div>
        <h1 class="h2 mb-1">Detalhes do Tutor</h1>
        <p class="text-body-secondary mb-0">
          Visualize os dados do tutor e cadastre pets vinculados.
        </p>
      </div>
      <RouterLink class="btn btn-outline-primary" :to="{ name: 'tutores' }">
        <i class="bi bi-arrow-left me-2" aria-hidden="true"></i>
        Voltar para Tutores
      </RouterLink>
    </header>

    <div v-if="erro" class="alert alert-danger" role="alert">{{ erro }}</div>
    <div v-if="carregando" class="text-body-secondary py-3" role="status">
      Carregando dados do tutor...
    </div>
    <template v-else-if="tutor">
      <section class="card shadow-sm mb-4">
        <div class="card-header bg-white">
          <h2 class="h5 mb-0">Informações do Tutor</h2>
        </div>
        <div class="card-body">
          <section class="card mb-3">
            <div class="card-header bg-light">
              <h3 class="h6 mb-0">Dados do Tutor</h3>
            </div>
            <div class="card-body">
              <dl class="row mb-0">
                <div class="col-12 col-md-4 mb-3">
                  <dt>ID</dt>
                  <dd class="mb-0">{{ tutor.id }}</dd>
                </div>
                <div class="col-12 col-md-4 mb-3">
                  <dt>Nome Completo</dt>
                  <dd class="mb-0">{{ tutor.nome }}</dd>
                </div>
                <div class="col-12 col-md-4 mb-3">
                  <dt>CPF / CNPJ</dt>
                  <dd class="mb-0">{{ documentoMascarado(tutor.cpfCnpj) }}</dd>
                </div>
                <div class="col-12 col-md-4">
                  <dt>Telefone / Celular / WhatsApp</dt>
                  <dd class="mb-0">{{ valorOuTraco(tutor.telefone) }}</dd>
                </div>
                <div class="col-12 col-md-4">
                  <dt>E-mail</dt>
                  <dd class="mb-0">{{ valorOuTraco(tutor.email) }}</dd>
                </div>
                <div class="col-12 col-md-4">
                  <dt>Data de Nascimento</dt>
                  <dd class="mb-0">{{ dataFormatada(tutor.dataNascimento) }}</dd>
                </div>
              </dl>
            </div>
          </section>

          <section class="card">
            <div class="card-header bg-light">
              <h3 class="h6 mb-0">Endereço</h3>
            </div>
            <div class="card-body">
              <dl class="row mb-0">
                <div class="col-12 col-md-4 mb-3">
                  <dt>Rua</dt>
                  <dd class="mb-0">{{ valorOuTraco(tutor.rua) }}</dd>
                </div>
                <div class="col-12 col-md-4 mb-3">
                  <dt>Número</dt>
                  <dd class="mb-0">{{ valorOuTraco(tutor.numero) }}</dd>
                </div>
                <div class="col-12 col-md-4 mb-3">
                  <dt>Bairro</dt>
                  <dd class="mb-0">{{ valorOuTraco(tutor.bairro) }}</dd>
                </div>
                <div class="col-12 col-md-4">
                  <dt>Cidade</dt>
                  <dd class="mb-0">{{ valorOuTraco(tutor.cidade) }}</dd>
                </div>
                <div class="col-12 col-md-4">
                  <dt>Estado</dt>
                  <dd class="mb-0">{{ valorOuTraco(tutor.estado) }}</dd>
                </div>
                <div class="col-12 col-md-4">
                  <dt>CEP</dt>
                  <dd class="mb-0">{{ valorOuTraco(tutor.cep) }}</dd>
                </div>
              </dl>
            </div>
          </section>
        </div>
      </section>

      <section class="card shadow-sm mb-4">
        <div class="card-header bg-white">
          <h2 class="h5 mb-0">Pets do Tutor</h2>
        </div>
        <div class="card-body">
          <div class="row g-3">
            <div class="col-12 col-xl-6">
              <section class="card h-100">
                <div class="card-header bg-light d-flex align-items-center gap-2">
                  <h3 class="h6 mb-0">Pets vinculados</h3>
                  <span class="badge text-bg-primary">
                    {{ pets.length }} {{ pets.length === 1 ? 'pet' : 'pets' }}
                  </span>
                </div>
                <div class="table-responsive">
                  <table class="table table-striped table-hover align-middle mb-0">
                    <thead class="table-light">
                      <tr>
                        <th scope="col">ID</th>
                        <th scope="col">Nome</th>
                        <th scope="col">Espécie</th>
                        <th scope="col">Ações</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="pet in pets" :key="pet.id">
                        <td>{{ pet.id }}</td>
                        <td>{{ pet.nome }}</td>
                        <td>{{ pet.especie }}</td>
                        <td>
                          <RouterLink
                            class="btn btn-sm btn-outline-primary"
                            :to="{ name: 'detalhes-pet', params: { id: pet.id } }"
                          >
                            Visualizar Pet
                          </RouterLink>
                        </td>
                      </tr>
                      <tr v-if="pets.length === 0">
                        <td colspan="4" class="text-center text-body-secondary py-4">
                          Nenhum pet vinculado a este tutor.
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </section>
            </div>

            <div class="col-12 col-xl-6">
              <section class="card h-100">
                <div class="card-header bg-white">
                  <h3 class="h6 mb-1">Cadastrar novo pet</h3>
                  <p class="text-body-secondary small mb-0">
                    O pet será vinculado automaticamente a {{ tutor.nome }}.
                  </p>
                </div>
                <div class="card-body">
                  <form class="d-grid gap-3" @submit.prevent="cadastrarPet">
                    <div>
                      <label for="nome-pet" class="form-label">Nome do pet</label>
                      <input
                        id="nome-pet"
                        v-model.trim="novoPet.nome"
                        class="form-control"
                        type="text"
                        placeholder="Digite o nome do pet"
                        required
                      />
                    </div>
                    <div>
                      <label for="especie-pet" class="form-label">Espécie</label>
                      <select
                        id="especie-pet"
                        v-model="novoPet.especie"
                        class="form-select"
                        required
                      >
                        <option value="" disabled>Selecione</option>
                        <option value="Cachorro">Cachorro</option>
                        <option value="Gato">Gato</option>
                      </select>
                    </div>
                    <button
                      class="btn btn-success"
                      type="submit"
                      :disabled="!formularioPetValido || cadastrandoPet"
                    >
                      {{ cadastrandoPet ? 'Cadastrando...' : 'Cadastrar pet' }}
                    </button>
                  </form>
                </div>
              </section>
            </div>
          </div>
        </div>
      </section>

      <button
        class="btn btn-outline-danger mb-4"
        type="button"
        :disabled="removendoTutor"
        @click="excluirTutor"
      >
        {{ removendoTutor ? 'Removendo...' : 'Remover Tutor' }}
      </button>
    </template>
  </div>
</template>
