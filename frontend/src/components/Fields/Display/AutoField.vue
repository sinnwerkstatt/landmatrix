<template>
  <div class="auto_field">
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

<script lang="ts">
  import Vue, { PropType } from "vue";
  import type { FormField } from "$components/Fields/fields";

  export default Vue.extend({
    props: {
      formfield: { type: Object as PropType<FormField>, required: true },
      value: { type: Number, required: true },
      model: { type: String, required: true },
      targetBlank: { type: Boolean, default: false },
    },
  });
</script>
