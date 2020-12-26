<template>
  <div>
    <router-link
      v-if="formfield.related_model === 'Investor'"
      class="investor"
      target="_blank"
      :to="{ name: 'investor_detail', params: { investorId: value.id } }"
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
    props: {
      formfield: { type: Object, required: true },
      value: { type: Object, required: true },
      model: { type: String, required: true },
    },
  };
</script>
