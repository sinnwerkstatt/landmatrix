<template>
  <div class="row">
    <div class="col-12">
      <div v-html="value"></div>
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
