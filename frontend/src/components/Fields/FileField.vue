<template>
  <div>
    <div v-if="readonly">
    <a :href="`${MEDIA_URL}${val}`" target="_blank">
      <i class="fa fa-file-pdf-o" aria-hidden="true"></i>TODO
    </a>

    </div>
  </div>
</template>

<script>

  export default {
    props: ["formfield", "value", "readonly"],
    data() {
      return {
        val: this.value,
        MEDIA_URL: MEDIA_URL,
      };
    },
    methods: {
      emitVal() {
        this.$emit("input", this.val);
      },

    },
  };
</script>
