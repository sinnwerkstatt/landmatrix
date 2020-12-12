<template>
  <div>
    <a :href="`${MEDIA_URL}${value}`" target="_blank">
      <i class="far fa-file-pdf"></i>
      {{ value }}
    </a>
  </div>
</template>

<script>
  export default {
    props: ["formfield", "value", "model"],
    data() {
      return {
        MEDIA_URL: MEDIA_URL,
      };
    },
  };
</script>
