<template>
  <div>
    <router-link
      v-if="model === 'deal'"
      class="id-display deal-id-display"
      :to="{ name: 'deal_detail', params: { dealId: value } }"
      >{{ value }}</router-link
    >
    <router-link
      v-else-if="model === 'investor'"
      class="id-display investor-id-display"
      :to="{ name: 'investor_detail', params: { investorId: value } }"
      >{{ value }}</router-link
    >
    <span v-else>{{ value }}</span>
  </div>
</template>

<script>
  export default {
    props: {
      formfield: { type: Object, required: true },
      value: { type: Number, required: true },
      model: { type: String, required: true },
    },
  };
</script>
