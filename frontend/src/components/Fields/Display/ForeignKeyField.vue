<template>
  <div>
    <router-link
      v-if="formfield.related_model === 'Investor'"
      :to="{ name: 'investor_detail', params: { investor_id: value.id } }"
      v-slot="{ href }"
    >
      <a :href="href">{{ value.name }} (#{{ value.id }})</a>
    </router-link>
    <template v-else>
      {{ value.name }}
    </template>
  </div>
</template>

<script>
  export default {
    props: ["formfield", "value"],
  };
</script>
