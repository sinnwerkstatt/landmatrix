<script lang="ts">
  import { gql } from "@apollo/client/core";
  import { _ } from "svelte-i18n";
  import { client } from "$lib/apolloClient";
  import FilePdfIcon from "$components/icons/FilePdfIcon.svelte";

  export let value;
  export let accept;

  function removeFile() {
    if (confirm($_("Do you really want to remove this file?")) === true) value = "";
  }

  export let uploadFunction = ({ target: { files = [] } }) => {
    if (!files.length) return;
    let fr = new FileReader();
    fr.onload = async () => {
      const { data } = await $client.mutate<{ upload_datasource_file: string }>({
        mutation: gql`
          mutation ($filename: String!, $payload: String!) {
            upload_datasource_file(filename: $filename, payload: $payload)
          }
        `,
        variables: { filename: files[0].name, payload: fr.result },
      });
      value = data.upload_datasource_file;
    };
    fr.readAsDataURL(files[0]);
  };
</script>

<div class="file_field">
  {#if value}
    <div class="flex w-full justify-between">
      <div>
        <a href="{import.meta.env.VITE_MEDIA_URL}{value}`" target="_blank">
          <FilePdfIcon />
          {value.replace("uploads/", "")}
        </a>
        <br />
        {$_("Change")}:
        <input type="file" on:change={uploadFunction} {accept} />
      </div>

      <button class="btn btn-danger" on:click|preventDefault={removeFile}>
        {$_("Remove this file")}
      </button>
    </div>
  {:else}
    <input type="file" on:change={uploadFunction} {accept} />
  {/if}
  <small class="text-gray-500 block pt-2">{$_("Maximum file size: 10MB")}</small>
</div>
