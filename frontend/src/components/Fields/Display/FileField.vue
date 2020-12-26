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
    props: {
      formfield: { type: Object, required: true },
      value: { type: String, required: true },
      model: { type: String, required: true },
    },
    data() {
      return {
        // eslint-disable-next-line no-undef
        MEDIA_URL: MEDIA_URL,
      };
    },
  };
</script>
