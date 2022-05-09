<template>
  <div class="typed_choice_field">
    {{ parseVal(value) }}
  </div>
</template>

<script lang="ts">
  import type { FormField } from "$components/Fields/fields";
  import { flatten_choices } from "$utils";
  import Vue from "vue";
  import type { PropType } from "vue";

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
