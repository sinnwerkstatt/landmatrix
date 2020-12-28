<template>
  <div class="row">
    <div class="col-12">
      <h3>{{ value }}</h3>
    </div>
  </div>
</template>

<script>
  export default {
    props: {
      value: { type: String, required: true },
    },
  };
</script>
