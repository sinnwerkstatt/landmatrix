<script lang="ts">
  import { gql } from "@urql/svelte";
  import { _ } from "svelte-i18n";
  import { page } from "$app/stores";
  import FilePdfIcon from "$components/icons/FilePdfIcon.svelte";

  export let value: string;
  export let accept: string;
  // "application/msword, application/vnd.ms-excel, application/vnd.ms-powerpoint," +
  // " text/plain, application/pdf, image/*";

  function removeFile() {
    if (confirm($_("Do you really want to remove this file?")) === true) value = "";
  }

  function uploadFile({ target: { files = [] } }) {
    if (!files.length) return;
    let fr = new FileReader();
    fr.onload = async () => {
      const { data } = await $page.data.urqlClient
        .mutation<{ upload_datasource_file: string }>(
          gql`
            mutation ($filename: String!, $payload: String!) {
              upload_datasource_file(filename: $filename, payload: $payload)
            }
          `,
          { filename: files[0].name, payload: fr.result }
        )
        .toPromise();
      value = data.upload_datasource_file;
    };
    fr.readAsDataURL(files[0]);
  }
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
        <input type="file" on:change={uploadFile} {accept} />
      </div>

      <button class="btn btn-danger" on:click|preventDefault={removeFile}>
        {$_("Remove this file")}
      </button>
    </div>
  {:else}
    <input type="file" on:change={uploadFile} {accept} />
  {/if}
  <small class="text-gray-500 block pt-2">{$_("Maximum file size: 10MB")}</small>
</div>
