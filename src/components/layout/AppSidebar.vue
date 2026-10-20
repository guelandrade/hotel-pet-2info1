<script setup>
import { RouterLink, useRoute } from 'vue-router';

const route = useRoute();
</script>

<template>
  <nav aria-label="Menu da PetSchool">
    <div class="nav flex-column nav-pills gap-1">
      <RouterLink
        class="nav-link"
        :class="{ active: route.name === 'pets' || route.name === 'detalhes-pet' }"
        to="/pets"
      >
        <i
          class="bi bi-heart me-2"
          aria-hidden="true"
        ></i>
        Pets
      </RouterLink>

      <RouterLink
        class="nav-link"
        :class="{ active: route.name === 'addPet' }"
        to="/pets/novo"
      >
        <i
          class="bi bi-plus-circle me-2"
          aria-hidden="true"
        ></i>
        Novo pet
      </RouterLink>

      <RouterLink
        class="nav-link"
        :class="{ active: route.name === 'tutores' || route.name === 'detalhes-tutor' }"
        to="/tutores"
      >
        <i
          class="bi bi-people me-2"
          aria-hidden="true"
        ></i>
        Tutores
      </RouterLink>
      <RouterLink
        class="nav-link"
        :class="{ active: route.name === 'addTutor' }"
        to="/tutores/novo"
      >
        <i
          class="bi bi-plus-circle me-2"
          aria-hidden="true"
        ></i>
        Novo tutor
      </RouterLink>
    </div>
  </nav>
</template>
