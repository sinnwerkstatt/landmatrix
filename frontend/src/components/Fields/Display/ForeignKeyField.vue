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
    <template v-else> {{ calc_name }} </template>
  </div>
</template>

<script>
  export default {
    props: {
      formfield: { type: Object, required: true },
      value: { type: Object, required: true },
      model: { type: String, required: true },
    },
    computed: {
      calc_name() {
        if (
          this.formfield.related_model === "Country" &&
          this.$store.state.page.countries
        ) {
          return this.$store.state.page.countries.find((c) => c.id === this.value.id)
            .name;
        }
        return this.value.username ?? this.value.name ?? this.value.id;
      },
    },
  };
</script>
