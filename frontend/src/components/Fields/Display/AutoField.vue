<template>
  <div>
    <router-link
      v-if="model === 'deal'"
      :to="{ name: 'deal_detail', params: { deal_id: value } }"
      >{{ value }}</router-link
    >
    <router-link
      v-if="model === 'investor'"
      :to="{ name: 'investor_detail', params: { investor_id: value } }"
      >{{ value }}</router-link
    >
    <span v-else>{{ value }}</span>
  </div>
</template>

<script>
  export default {
    props: ["formfield", "value", "model"],
  };
</script>
