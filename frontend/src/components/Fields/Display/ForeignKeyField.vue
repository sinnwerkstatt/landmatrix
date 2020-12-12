<template>
  <div>
    <router-link
      v-if="formfield.related_model === 'Investor'"
      target="_blank"
      :to="{ name: 'investor_detail', params: { investor_id: value.id } }"
    >
      {{ value.name }} (#{{ value.id }})
    </router-link>
    <template v-else>
      {{ value.name }}
    </template>
  </div>
</template>

<script>
  export default {
    props: ["formfield", "value", "model"],
  };
</script>
