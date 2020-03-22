<template>
  <div class="row widget-gallery">
    <div v-for="image in value.images" class="col">
      <wagtail-image :value="image" />
    </div>
  </div>
</template>

<script>
  export default {
    props: ["value"],
  };
</script>

<style scoped></style>
