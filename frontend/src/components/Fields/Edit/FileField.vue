<template>
  <div>
    <div v-if="value">
      Current:
      <a :href="`${MEDIA_URL}${value}`" target="_blank">
        <i class="far fa-file-pdf"></i>
        {{ value.replace("uploads/", "") }}
      </a>
      <br />
      Change: <input type="file" :name="formfield.name" /><br />
      <label>
        Clear file
        <input type="checkbox" :name="`clear_${formfield.name}`" />
      </label>
    </div>
    <div v-else>
      <input type="file" :name="formfield.name" />
    </div>
  </div>
</template>

<script>
  export default {
    props: {
      formfield: { type: Object, required: true },
      value: { type: String, required: false },
      model: { type: String, required: true },
    },
    data() {
      return {
        // eslint-disable-next-line no-undef
        MEDIA_URL: MEDIA_URL,
        user: this.$store.state.page.user,
      };
    },
  };
</script>
