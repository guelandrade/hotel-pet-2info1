<script setup>
import { computed, reactive, ref } from 'vue';
import { RouterLink, useRouter } from 'vue-router';
import { apiFetch } from '@/services/api';

const router = useRouter();
const tutor = reactive({
  nome: '',
  cpfCnpj: '',
  telefone: '',
  email: '',
  dataNascimento: '',
  rua: '',
  numero: '',
  bairro: '',
  cidade: '',
  estado: '',
  cep: '',
});
const salvando = ref(false);
const buscandoCep = ref(false);
const erro = ref('');
const erroCep = ref('');
const camposVisitados = reactive({
  nome: false,
  cpfCnpj: false,
  telefone: false,
  email: false,
  dataNascimento: false,
});

const estados = [
  'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS',
  'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC',
  'SP', 'SE', 'TO',
];

function somenteDigitos(valor) {
  return valor.replace(/\D/g, '');
}

function formatarTelefone(valor) {
  const digitos = somenteDigitos(valor).slice(0, 11);
  if (digitos.length <= 2) return digitos ? `(${digitos}` : '';
  if (digitos.length <= 6) return `(${digitos.slice(0, 2)}) ${digitos.slice(2)}`;
  const tamanhoPrefixo = digitos.length === 11 ? 7 : 6;
  return `(${digitos.slice(0, 2)}) ${digitos.slice(2, tamanhoPrefixo)}-${digitos.slice(tamanhoPrefixo)}`;
}

function formatarDocumento(valor) {
  const digitos = somenteDigitos(valor).slice(0, 14);
  if (digitos.length <= 11) {
    return `${digitos.slice(0, 3)}${digitos.length > 3 ? `.${digitos.slice(3, 6)}` : ''}${digitos.length > 6 ? `.${digitos.slice(6, 9)}` : ''}${digitos.length > 9 ? `-${digitos.slice(9, 11)}` : ''}`;
  }
  return `${digitos.slice(0, 2)}.${digitos.slice(2, 5)}.${digitos.slice(5, 8)}/${digitos.slice(8, 12)}${digitos.length > 12 ? `-${digitos.slice(12, 14)}` : ''}`;
}

function formatarCep(valor) {
  const digitos = somenteDigitos(valor).slice(0, 8);
  return digitos.length > 5
    ? `${digitos.slice(0, 5)}-${digitos.slice(5)}`
    : digitos;
}

function documentoValido(digitos) {
  if (digitos.length === 11) {
    if (/^(\d)\1+$/.test(digitos)) return false;
    let soma = 0;
    for (let indice = 0; indice < 9; indice += 1) {
      soma += Number(digitos[indice]) * (10 - indice);
    }
    let digito = (soma * 10) % 11;
    if (digito === 10) digito = 0;
    if (digito !== Number(digitos[9])) return false;

    soma = 0;
    for (let indice = 0; indice < 10; indice += 1) {
      soma += Number(digitos[indice]) * (11 - indice);
    }
    digito = (soma * 10) % 11;
    if (digito === 10) digito = 0;
    return digito === Number(digitos[10]);
  }

  if (digitos.length === 14) {
    if (/^(\d)\1+$/.test(digitos)) return false;
    const calcularDigito = (base, pesos) => {
      const soma = base
        .split('')
        .reduce((total, numero, indice) => total + Number(numero) * pesos[indice], 0);
      const resto = soma % 11;
      return resto < 2 ? 0 : 11 - resto;
    };
    const primeiro = calcularDigito(digitos.slice(0, 12), [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]);
    const segundo = calcularDigito(digitos.slice(0, 12) + primeiro, [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]);
    return digitos.endsWith(`${primeiro}${segundo}`);
  }

  return false;
}

const nomeInvalido = computed(() => !tutor.nome.trim());
const telefoneInvalido = computed(() => ![10, 11].includes(somenteDigitos(tutor.telefone).length));
const emailInvalido = computed(
  () => Boolean(tutor.email) && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(tutor.email),
);
const documentoInvalido = computed(() => {
  const digitos = somenteDigitos(tutor.cpfCnpj);
  return Boolean(digitos) && !documentoValido(digitos);
});
const dataInvalida = computed(() => {
  if (!tutor.dataNascimento) return false;
  const hoje = new Date();
  const dataLimite = `${hoje.getFullYear()}-${String(hoje.getMonth() + 1).padStart(2, '0')}-${String(hoje.getDate()).padStart(2, '0')}`;
  return tutor.dataNascimento > dataLimite;
});
const formularioValido = computed(
  () =>
    !nomeInvalido.value &&
    !telefoneInvalido.value &&
    !emailInvalido.value &&
    !documentoInvalido.value &&
    !dataInvalida.value,
);
const formularioFoiRevisado = computed(
  () => Object.values(camposVisitados).some(Boolean) && !formularioValido.value,
);

function atualizarTelefone(evento) {
  tutor.telefone = formatarTelefone(evento.target.value);
}

function atualizarDocumento(evento) {
  tutor.cpfCnpj = formatarDocumento(evento.target.value);
}

function atualizarCep(evento) {
  tutor.cep = formatarCep(evento.target.value);
  erroCep.value = '';
}

async function buscarCep() {
  const cep = somenteDigitos(tutor.cep);
  if (!cep) return;
  if (cep.length !== 8) {
    erroCep.value = 'Informe um CEP com 8 dígitos.';
    return;
  }

  buscandoCep.value = true;
  erroCep.value = '';
  try {
    const resposta = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
    if (!resposta.ok) {
      throw new Error('Não foi possível consultar o CEP. Tente novamente.');
    }
    const endereco = await resposta.json();
    if (endereco.erro) {
      erroCep.value = 'CEP não encontrado. Confira os números e tente novamente.';
      return;
    }
    tutor.rua = endereco.logradouro ?? '';
    tutor.bairro = endereco.bairro ?? '';
    tutor.cidade = endereco.localidade ?? '';
    tutor.estado = endereco.uf ?? '';
  } catch (error) {
    erroCep.value = error instanceof TypeError
      ? 'Não foi possível conectar ao ViaCEP. Confira sua conexão e tente novamente.'
      : error instanceof Error
        ? error.message
        : 'Não foi possível consultar o CEP. Tente novamente.';
  } finally {
    buscandoCep.value = false;
  }
}

async function salvarTutor() {
  if (!formularioValido.value) return;

  salvando.value = true;
  erro.value = '';
  try {
    const resposta = await apiFetch('/tutores', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...tutor,
        nome: tutor.nome.trim(),
        telefone: tutor.telefone.trim(),
      }),
    });
    if (!resposta.ok) {
      throw new Error('Não foi possível cadastrar o tutor. Tente novamente.');
    }
    await router.push({ name: 'tutores' });
  } catch (error) {
    erro.value = error instanceof Error
      ? error.message
      : 'Não foi possível cadastrar o tutor. Tente novamente.';
  } finally {
    salvando.value = false;
  }
}
</script>

<template>
  <div class="container-fluid">
    <header class="d-flex flex-wrap align-items-center justify-content-between gap-3 mb-4">
      <div>
        <h1 class="h2 mb-1">Cadastrar Tutor</h1>
        <p class="text-body-secondary mb-0">Preencha os dados para cadastrar um novo tutor.</p>
      </div>
    </header>

    <form @submit.prevent="salvarTutor">
      <section class="card shadow-sm mb-4">
        <div class="card-header bg-white">
          <h2 class="h5 mb-0">Dados do Tutor</h2>
        </div>
        <div class="card-body">
          <div class="row g-3">
            <div class="col-12 col-md-4">
              <label for="id-tutor" class="form-label">ID</label>
              <input
                id="id-tutor"
                class="form-control"
                type="text"
                placeholder="Gerado automaticamente"
                disabled
              />
            </div>
            <div class="col-12 col-md-8">
              <label for="nome-tutor" class="form-label">Nome Completo</label>
              <input
                id="nome-tutor"
                v-model="tutor.nome"
                class="form-control"
                :class="{ 'is-invalid': camposVisitados.nome && nomeInvalido }"
                type="text"
                placeholder="Digite o nome completo"
                autocomplete="name"
                required
                @blur="camposVisitados.nome = true"
              />
              <div v-if="camposVisitados.nome && nomeInvalido" class="invalid-feedback">
                Ops, campo obrigatório, por favor preencha-o!
              </div>
            </div>
            <div class="col-12 col-md-6">
              <label for="cpf-cnpj" class="form-label">CPF / CNPJ</label>
              <input
                id="cpf-cnpj"
                class="form-control"
                :class="{ 'is-invalid': camposVisitados.cpfCnpj && documentoInvalido }"
                type="text"
                inputmode="numeric"
                placeholder="Digite o CPF ou CNPJ"
                :value="tutor.cpfCnpj"
                @input="atualizarDocumento"
                @blur="camposVisitados.cpfCnpj = true"
              />
              <div class="form-text">A máscara muda conforme 11 dígitos (CPF) ou 14 dígitos (CNPJ).</div>
              <div v-if="camposVisitados.cpfCnpj && documentoInvalido" class="invalid-feedback">
                Informe um CPF ou CNPJ válido.
              </div>
            </div>
            <div class="col-12 col-md-6">
              <label for="telefone-tutor" class="form-label">Telefone / Celular / WhatsApp</label>
              <input
                id="telefone-tutor"
                class="form-control"
                :class="{ 'is-invalid': camposVisitados.telefone && telefoneInvalido }"
                type="tel"
                inputmode="tel"
                placeholder="(00) 00000-0000"
                autocomplete="tel"
                :value="tutor.telefone"
                required
                @input="atualizarTelefone"
                @blur="camposVisitados.telefone = true"
              />
              <div class="form-text">Formato: (00) 00000-0000</div>
              <div v-if="camposVisitados.telefone && telefoneInvalido" class="invalid-feedback">
                Informe um telefone válido com DDD.
              </div>
            </div>
            <div class="col-12 col-md-6">
              <label for="email-tutor" class="form-label">E-mail</label>
              <input
                id="email-tutor"
                v-model.trim="tutor.email"
                class="form-control"
                :class="{ 'is-invalid': camposVisitados.email && emailInvalido }"
                type="email"
                placeholder="nome@example.com"
                autocomplete="email"
                @blur="camposVisitados.email = true"
              />
              <div v-if="camposVisitados.email && emailInvalido" class="invalid-feedback">
                Informe um e-mail válido.
              </div>
            </div>
            <div class="col-12 col-md-6">
              <label for="nascimento-tutor" class="form-label">Data de Nascimento</label>
              <input
                id="nascimento-tutor"
                v-model="tutor.dataNascimento"
                class="form-control"
                :class="{ 'is-invalid': camposVisitados.dataNascimento && dataInvalida }"
                type="date"
                autocomplete="bday"
                @blur="camposVisitados.dataNascimento = true"
              />
              <div v-if="camposVisitados.dataNascimento && dataInvalida" class="invalid-feedback">
                A data de nascimento não pode ser futura.
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="card shadow-sm mb-4">
        <div class="card-header bg-white">
          <h2 class="h5 mb-0">Endereço</h2>
        </div>
        <div class="card-body">
          <div class="row g-3">
            <div class="col-12 col-md-4">
              <label for="cep-tutor" class="form-label">CEP</label>
              <input
                id="cep-tutor"
                class="form-control"
                :class="{ 'is-invalid': Boolean(erroCep) }"
                type="text"
                inputmode="numeric"
                placeholder="00000-000"
                autocomplete="postal-code"
                :value="tutor.cep"
                @input="atualizarCep"
                @blur="buscarCep"
              />
              <div class="form-text">{{ buscandoCep ? 'Consultando CEP...' : 'Preencha o CEP para buscar o endereço.' }}</div>
              <div v-if="erroCep" class="invalid-feedback">{{ erroCep }}</div>
            </div>
            <div class="col-12 col-md-6">
              <label for="rua-tutor" class="form-label">Rua</label>
              <input
                id="rua-tutor"
                v-model.trim="tutor.rua"
                class="form-control"
                type="text"
                placeholder="Digite o nome da rua"
                autocomplete="address-line1"
              />
            </div>
            <div class="col-12 col-md-2">
              <label for="numero-tutor" class="form-label">Número</label>
              <input
                id="numero-tutor"
                v-model.trim="tutor.numero"
                class="form-control"
                type="text"
                placeholder="Número"
                autocomplete="address-line2"
              />
            </div>
            <div class="col-12 col-md-6">
              <label for="bairro-tutor" class="form-label">Bairro</label>
              <input
                id="bairro-tutor"
                v-model.trim="tutor.bairro"
                class="form-control"
                type="text"
                placeholder="Digite o bairro"
              />
            </div>
            <div class="col-12 col-md-4">
              <label for="cidade-tutor" class="form-label">Cidade</label>
              <input
                id="cidade-tutor"
                v-model.trim="tutor.cidade"
                class="form-control"
                type="text"
                placeholder="Digite a cidade"
                autocomplete="address-level2"
              />
            </div>
            <div class="col-12 col-md-2">
              <label for="estado-tutor" class="form-label">Estado</label>
              <select
                id="estado-tutor"
                v-model="tutor.estado"
                class="form-select"
                autocomplete="address-level1"
              >
                <option value="">Selecione</option>
                <option v-for="estado in estados" :key="estado" :value="estado">
                  {{ estado }}
                </option>
              </select>
            </div>
          </div>
        </div>
      </section>

      <div v-if="erro" class="alert alert-danger" role="alert">{{ erro }}</div>
      <div v-if="formularioFoiRevisado" class="alert alert-info" role="status">
        Preencha corretamente Nome e Telefone e revise os campos informados para habilitar o cadastro.
      </div>
      <div class="d-flex flex-wrap justify-content-end gap-2 mb-4">
        <RouterLink class="btn btn-outline-secondary" :to="{ name: 'tutores' }">
          Cancelar
        </RouterLink>
        <button class="btn btn-primary" type="submit" :disabled="!formularioValido || salvando">
          {{ salvando ? 'Cadastrando...' : 'Cadastrar Tutor' }}
        </button>
      </div>
    </form>
  </div>
</template>
