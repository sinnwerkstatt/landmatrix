<template>
  <div>
    <template v-if="formfield.related_model === 'Investor'">
      <template v-for="val in value">
        <router-link
          class="investor"
          target="_blank"
          :to="{ name: 'investor_detail', params: { investorId: val.id } }"
        >
          {{ val.name }} (#{{ val.id }})
        </router-link>
        <br :key="val.id" />
      </template>
    </template>
    <template v-else>
      {{ value }}
    </template>
  </div>
</template>

<script lang="ts">
  import type { PropType } from "vue";
  import type { FormField } from "$components/Fields/fields";
  import Vue from "vue";

  export default Vue.extend({
    name: "ManyToManyField",
    props: {
      formfield: { type: Object as PropType<FormField>, required: true },
      value: { type: [Array, Object], required: true },
      model: { type: String, required: true },
    },
  });
</script>
