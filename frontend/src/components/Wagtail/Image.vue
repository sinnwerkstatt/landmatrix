<template>
  <div class="widget-image">
    <a v-if="link" :href="link" :target="external">
      <img :src="path" class="image" :alt="alt" />
    </a>
    <img v-else :src="path" class="image" :alt="alt" />

    <div v-if="caption" class="carousel-caption">{{ caption }}</div>
  </div>
  <!-- widget-image -->
</template>

<script>
  export default {
    props: ["value"],
    data() {
      return {
        path: null,
        link: null,
        alt: null,
        external: false,
        caption: null,
      };
    },
    created() {
      let image_id = this.value.image ? this.value.image : this.value;
      this.link = this.value.url;
      let url = `/wagtailapi/v2/images/${image_id}`;
      this.$http.get(url).then((response) => {
        let meta = response.body.meta;
        this.path = meta.download_url;
      });
    },
  };
</script>

<style lang="scss">
  img {
    width: 100%;
    max-width: 100%;
  }
  .widget-image {
    margin-bottom: 20px;
  }
</style>
