<template>
  <div class="form-field row" v-if="!file_not_public || user.is_authenticated">
    <div class="label" :class="labelClasses">
      {{ formfield.label }}
    </div>
    <div class="val" :class="valClasses">
      <div v-if="readonly">
        <a :href="`${MEDIA_URL}${val}`" target="_blank">
          <i :class="[file_not_public ? 'fas' : 'far', 'fa-file-pdf']"></i>
        </a>
      </div>
    </div>
  </div>
</template>

<script>
  import { fieldMixin } from "./fieldMixin";

  export default {
    mixins: [fieldMixin],
    data() {
      return {
        MEDIA_URL: MEDIA_URL,
        user: this.$store.state.page.user,
      };
    },
  };
</script>
