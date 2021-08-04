<template>
  <div>
    <router-link
      v-if="model === 'deal'"
      class="id-display deal-id-display"
      :to="{ name: 'deal_detail', params: { dealId: value } }"
      :target="targetBlank ? '_blank' : '_self'"
      >{{ value }}</router-link
    >
    <router-link
      v-else-if="model === 'investor'"
      class="id-display investor-id-display"
      :to="{ name: 'investor_detail', params: { investorId: value } }"
      :target="targetBlank ? '_blank' : '_self'"
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
      targetBlank: { type: Boolean, default: false },
    },
  };
</script>
