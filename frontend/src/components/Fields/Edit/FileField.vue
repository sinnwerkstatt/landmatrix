<template>
  <div>
    <div v-if="value">
      <a :href="`${media_url}${value}`" target="_blank">
        <i class="far fa-file-pdf"></i>
        {{ value.replace("uploads/", "") }}
      </a>
      <br />
      Change:
      <input
        style="display: inline"
        type="file"
        :name="formfield.name"
        @change="uploadFile"
      /><br />
      <a href="#" @click.prevent="removeFile">Remove this file</a>
    </div>
    <div v-else>
      <input type="file" :name="formfield.name" @change="uploadFile" />
    </div>
  </div>
</template>

<script>
  import gql from "graphql-tag";

  export default {
    props: {
      formfield: { type: Object, required: true },
      value: { type: String, required: false, default: "" },
      model: { type: String, required: true },
    },
    data() {
      return {
        media_url: import.meta.env.VITE_MEDIA_URL,
        user: this.$store.state.user,
      };
    },
    methods: {
      removeFile() {
        if (confirm(this.$t("Do you really want to remove this file?")) === true) {
          this.$emit("input", "");
        }
      },
      uploadFile({ target: { files = [] } }) {
        if (!files.length) return;
        let fr = new FileReader();
        fr.onload = () => {
          this.$apollo
            .mutate({
              mutation: gql`
                mutation ($filename: String!, $payload: String!) {
                  upload_datasource_file(filename: $filename, payload: $payload)
                }
              `,
              variables: {
                filename: files[0].name,
                payload: fr.result,
              },
            })
            .then(({ data: { upload_datasource_file } }) => {
              this.$emit("input", upload_datasource_file);
            });
        };
        fr.readAsDataURL(files[0]);
      },
    },
  };
</script>

<style lang="scss" scoped>
  input {
    width: 100%;
    max-width: 100%;
  }
</style>
