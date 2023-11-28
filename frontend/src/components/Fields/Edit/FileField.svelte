<script lang="ts">
  import { Client, gql } from "@urql/svelte"
  import { _ } from "svelte-i18n"
  import type { ChangeEventHandler } from "svelte/elements"

  import { page } from "$app/stores"

  import type { FormField } from "$components/Fields/fields"
  import FilePdfIcon from "$components/icons/FilePdfIcon.svelte"

  export let value: string
  export let formfield: FormField
  export let accept =
    "application/msword, " +
    "application/vnd.ms-excel, " +
    "application/vnd.ms-powerpoint, " +
    "text/plain, " +
    "application/pdf, " +
    "image/*"

  const removeFile = () => {
    if (confirm($_("Do you really want to remove this file?"))) {
      value = ""
    }
  }

  const uploadFile: ChangeEventHandler<HTMLInputElement> = ({
    currentTarget: { files },
  }) => {
    if (!files || !files.length) return

    let fr = new FileReader()
    fr.onload = async () => {
      const { error, data } = await ($page.data.urqlClient as Client)
        .mutation<{ upload_datasource_file: string }>(
          gql`
            mutation ($filename: String!, $payload: String!) {
              upload_datasource_file(filename: $filename, payload: $payload)
            }
          `,
          { filename: files[0].name, payload: fr.result },
        )
        .toPromise()

      if (error || !data) {
        alert(`Error uploading file: ${files[0].name}`)
      } else {
        value = data.upload_datasource_file
      }
    }
    fr.readAsDataURL(files[0])
  }
</script>

{#if value}
  <div class="flex w-full justify-between">
    <div>
      <a
        href="{import.meta.env.VITE_MEDIA_URL}{value}"
        target="_blank"
        rel="noreferrer"
      >
        <FilePdfIcon />
        {value.replace("uploads/", "")}
      </a>
      <br />
      {$_("Change")}:
      <input type="file" name={formfield.name} on:change={uploadFile} {accept} />
    </div>

    <button class="btn btn-danger" on:click|preventDefault={removeFile}>
      {$_("Remove this file")}
    </button>
  </div>
{:else}
  <input type="file" name={formfield.name} on:change={uploadFile} {accept} />
{/if}
<small class="block pt-2 text-gray-500">{$_("Maximum file size: 10MB")}</small>
