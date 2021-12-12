<template>
  <div class="foreignkey_field">
    <router-link
      v-if="formfield.related_model === 'Investor'"
      class="investor"
      target="_blank"
      :to="{ name: 'investor_detail', params: { investorId: value.id } }"
    >
      {{ value.name }} (#{{ value.id }})
    </router-link>
    <template v-else> {{ calc_name }} </template>
  </div>
</template>

<script lang="ts">
  import Vue, { PropType } from "vue";
  import type { FormField } from "$components/Fields/fields";
  import type { Country } from "$types/wagtail";

  export default Vue.extend({
    props: {
      formfield: { type: Object as PropType<FormField>, required: true },
      value: { type: Object, required: true },
      model: { type: String, required: true },
    },
    computed: {
      calc_name(): string {
        if (!this.value || !this.value.id) return "";
        if (this.formfield.related_model === "Country" && this.$store.state.countries) {
          return this.$store.state.countries.find(
            (c: Country) => c.id === this.value.id
          ).name;
        }
        return this.value.username ?? this.value.name ?? this.value.id;
      },
    },
  });
</script>
