<template>
  <div>
    <a :href="`${media_url}${value}`" target="_blank">
      <i v-if="fileNotPublic" class="fas fa-eye-slash mr-1"></i>
      <i class="far fa-file-pdf"></i>
      {{ value.replace("uploads/", "") }}
    </a>
  </div>
</template>

<script>
  export default {
    props: {
      formfield: { type: Object, required: true },
      value: { type: String, required: true },
      model: { type: String, required: true },
      fileNotPublic: { type: Boolean, default: false },
    },
    data() {
      return { media_url: import.meta.env.VITE_MEDIA_URL };
    },
  };
</script>
