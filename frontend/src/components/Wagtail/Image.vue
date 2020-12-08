<template>
  <div class="widget-image row">
    <div class="col-12">
      <a v-if="link" :href="link" :target="{ _blank: external }">
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
      <div v-if="caption" class="carousel-caption" v-html="caption" />
    </div>
  </div>
</template>

<script>
  export default {
    props: ["value"],
    data() {
      return {
        alt: null,
      };
    },
    computed: {
      link() {
        return this.value.image ? this.value.url : null;
      },
      path() {
        return this.value.image ? this.value.image.url : this.value.url;
      },
      caption() {
        return this.value.image ? this.value.caption : null;
      },
      external() {
        return this.value.image ? this.value.external : false;
      },
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

  .carousel-caption {
    bottom: 0;
    padding: 0 !important;
    text-shadow: none !important;

    p {
      background-color: rgba(0, 0, 0, 0.75);
      color: white;
      display: inline-block;
      padding: 0.2em 0.6em 0.3em;
    }
  }
</style>
