<template>
  <div>
    {{ display_status }}
  </div>
</template>

<script>
  import { draft_status_map, status_map } from "$utils/choices";

  export default {
    props: {
      formfield: { type: Object, required: true },
      value: { type: Array, required: true },
      model: { type: String, required: true },
    },
    computed: {
      display_status() {
        return this.value[1]
          ? draft_status_map[this.value[1]]
          : status_map[this.value[0]];
      },
    },
    methods: {},
  };
</script>
