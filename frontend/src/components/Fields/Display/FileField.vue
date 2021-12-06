<template>
  <div class="file_field">
    <a :href="`${media_url}${value}`" target="_blank">
      <i v-if="fileNotPublic" class="fas fa-eye-slash mr-1"></i>
      <i class="far fa-file-pdf"></i>
      {{ value.replace("uploads/", "") }}
    </a>
  </div>
</template>

<script lang="ts">
  import Vue, { PropType } from "vue";
  import type { FormField } from "$components/Fields/fields";

  export default Vue.extend({
    props: {
      formfield: { type: Object as PropType<FormField>, required: true },
      value: { type: String, required: true },
      model: { type: String, required: true },
      fileNotPublic: { type: Boolean, default: false },
    },
    data() {
      return { media_url: import.meta.env.VITE_MEDIA_URL };
    },
  });
</script>
