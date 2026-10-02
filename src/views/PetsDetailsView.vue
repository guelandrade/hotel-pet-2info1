<script setup>
  import { onMounted, ref } from 'vue';
import { useRoute, RouterLink } from 'vue-router';

  const route = useRoute();
  const API_URL = 'http://localhost:3000'
  // exibir informações do pet e do tutor
  const pet = ref(({}));
  const tutor = ref(([]));

  async function carregarPet() {
    // exibindo os dados do Id do pet
    const idPet = route.params.id;
    console.log('ID do pet:', idPet);

    const respostaPet = await fetch(`${API_URL}/pets/${idPet}`);
    pet.value = await respostaPet.json();

    const respostaTutor = await fetch(`${API_URL}/tutores/${pet.value.tutorId}`);
    tutor.value = await respostaTutor.json();
    console.log('Tutor:', tutor.value);
  }

  onMounted(carregarPet);
</script>

<template>
  <h1> Nome do pet: {{ pet.nome }} </h1>
  <p> Espécie: {{ pet.especie }} </p>
  <p> Tutor: {{ tutor?.nome }} </p>

  <button class="btn btn-default">
    <RouterLink :to="{name: 'pets' }">Voltar</RouterLink>
  </button>
</template>
