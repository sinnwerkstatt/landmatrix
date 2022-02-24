<template>
  <div class="text_field">
    <template v-if="formfield.class === 'URLField'">
      <a :href="value" target="_blank">{{ get_hostname(value) }}</a>
    </template>
    <template v-else>
      {{ parseVal(value) }}
    </template>
  </div>
</template>

<script lang="ts">
  import { flatten_choices } from "$utils";
  import Vue from "vue";
  import type { PropType } from "vue";
  import type { FormField } from "$components/Fields/fields";

  export default Vue.extend({
    props: {
      formfield: { type: Object as PropType<FormField>, required: true },
      value: { type: String, required: true },
      model: { type: String, required: true },
    },
    methods: {
      get_hostname(value: string): string {
        return new URL(value).hostname;
      },
      parseVal(val: string): string {
        if (!val) return "n/a";
        if (this.formfield.choices) {
          let choices = flatten_choices(this.formfield.choices, true);
          return choices ? choices[val] : val;
        }
        return val;
      },
    },
  });
</script>
