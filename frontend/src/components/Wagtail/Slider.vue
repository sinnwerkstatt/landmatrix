<template>
  <div class="slider">
    <b-carousel
      :id="value.id"
      :interval="3000"
      controls
      indicators
      style="width: 100%; height: 100%"
    >
      <b-carousel-slide v-for="image in value.images" :key="image.id">
        <template #img>
          <wagtail-image :value="image" />
        </template>
      </b-carousel-slide>
    </b-carousel>
  </div>
</template>

<script>
  export default {
    props: {
      value: { type: Object, required: true },
    },
  };
</script>

<style>
  .slider {
    margin: 0 auto;
    max-width: 600px;
    max-height: 800px;
  }
</style>
