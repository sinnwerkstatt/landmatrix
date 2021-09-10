<template>
  <span>{{ display_status }}</span>
</template>

<script>
  import { combined_status_fn, combined_status_options } from "$utils/choices";

  export default {
    props: {
      formfield: { type: Object, required: true },
      value: { type: Array, required: true },
      model: { type: String, required: true },
    },
    computed: {
      display_status() {
        return this.$t(
          combined_status_options[combined_status_fn(this.value[0], this.value[1])]
        );
      },
    },
    methods: {},
  };
</script>
