<template>
  <div>
    <div v-if="value">
      Current:
      <a :href="`${media_url}${value}`" target="_blank">
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
      value: { type: String, required: false, default: "" },
      model: { type: String, required: true },
    },
    data() {
      return {
        media_url: import.meta.env.VITE_MEDIA_URL,
        user: this.$store.state.page.user,
      };
    },
  };
</script>
