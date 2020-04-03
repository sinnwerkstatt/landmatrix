<template>
  <div class="widget-image">
    <a v-if="link" :href="link" :target="external">
      <img
        :src="path"
        class="image"
        :alt="alt"
        style="max-width: 100%; max-height: 100%;"
      />
    </a>
    <img
      v-else
      :src="path"
      class="image"
      :alt="alt"
      style="max-width: 100%; max-height: 100%;"
    />
    <div v-if="caption" class="carousel-caption">{{ caption }}</div>
  </div>
</template>

<script>
  import axios from 'axios';
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
      axios.get(url).then((response) => {
        let meta = response.data.meta;
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
