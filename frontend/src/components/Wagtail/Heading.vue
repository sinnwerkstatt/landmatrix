<template>
  <h3>{{ value }}</h3>
</template>

<script>
  export default {
    props: {
      value: { type: String, required: true },
    },
  };
</script>
