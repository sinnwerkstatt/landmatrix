<script lang="ts">
  import { env } from "$env/dynamic/public"
  import { _ } from "svelte-i18n"
  import type { ChangeEventHandler } from "svelte/elements"

  import { getCsrfToken } from "$lib/utils"

  import FilePdfIcon from "$components/icons/FilePdfIcon.svelte"

  export let value: string | null
  export let fieldname: string

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
      const ret = await fetch("/api/upload_datasource_file/", {
        method: "POST",
        credentials: "include",
        body: JSON.stringify({ filename: files[0].name, payload: fr.result }),
        headers: {
          "X-CSRFToken": await getCsrfToken(),
          "Content-Type": "application/json",
        },
      })
      if (ret.ok) {
        const retJson = await ret.json()
        value = retJson.name
      } else {
        alert(`Error uploading file: ${files[0].name}`)
      }
    }
    fr.readAsDataURL(files[0])
  }
</script>

{#if value}
  <div class="flex w-full justify-between">
    <div>
      <a
        href="{env.PUBLIC_MEDIA_URL ?? '/media/'}{value}"
        target="_blank"
        rel="noreferrer"
        class="flex w-full"
      >
        <FilePdfIcon />
        {#if value.length > 50}
          ...{value.replace("uploads/", "").slice(-50)}
        {:else}
          {value.replace("uploads/", "")}
        {/if}
      </a>
      <br />
      {$_("Change")}:
      <input type="file" on:change={uploadFile} {accept} />
    </div>

    <button
      class="butn-outline butn-flat butn-red"
      on:click|preventDefault={removeFile}
    >
      {$_("Remove this file")}
    </button>
  </div>
{:else}
  <input type="file" name={fieldname} on:change={uploadFile} {accept} />
{/if}
<small class="block pt-2 text-gray-500">{$_("Maximum file size: 10MB")}</small>
