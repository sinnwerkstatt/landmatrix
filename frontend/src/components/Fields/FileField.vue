<template>
  <div class="row" v-if="!file_not_public || user.is_authenticated">
    <div class="col-md-3 font-weight-bold">
      {{ formfield.label }}
    </div>
    <div class="col-md-9">
      <div v-if="readonly">
        <a :href="`${MEDIA_URL}${val}`" target="_blank">
          <i :class="[file_not_public ? 'fas' : 'far', 'fa-file-pdf']"></i>
        </a>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    props: ["formfield", "value", "readonly", "file_not_public"],
    data() {
      return {
        val: this.value,
        MEDIA_URL: MEDIA_URL,
        user: this.$store.state.page.user,
      };
    },
    methods: {
      emitVal() {
        this.$emit("input", this.val);
      },
    },
  };
</script>
