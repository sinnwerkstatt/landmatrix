<script lang="ts">
  import { env } from "$env/dynamic/public"
  import { _ } from "svelte-i18n"
  import type { ChangeEventHandler } from "svelte/elements"

  import { getCsrfToken } from "$lib/utils"

  import FilePdfIcon from "$components/icons/FilePdfIcon.svelte"

  export let value: string | null
  export let fieldname: string

  interface Extras {
    required?: boolean
  }

  export let extras: Extras = {
    required: false,
  }

  // would be nice to sync these with MIME type
  // https://www.npmjs.com/package/mime-db
  const ACCEPTED_EXTENSIONS: string[] = [
    ".pdf",
    ".xls",
    ".xlsx",
    ".jpg",
    ".png",
    ".mp4",
    ".mkv",
  ]

  const removeFile = () => {
    if (confirm($_("Do you really want to remove this file?"))) {
      value = ""
    }
  }

  const uploadFile: ChangeEventHandler<HTMLInputElement> = ({
    currentTarget: { files },
  }) => {
    if (!files || !files.length) return

    const file = files[0]
    const extension = file.name.split(".").pop()

    if (!extension || !ACCEPTED_EXTENSIONS.includes("." + extension)) {
      alert($_("Invalid file type: Check that your file type is supported."))
      return
    }

    const reader = new FileReader()

    reader.addEventListener("load", async () => {
      const ret = await fetch("/api/upload_datasource_file/", {
        method: "POST",
        credentials: "include",
        body: JSON.stringify({ filename: file.name, payload: reader.result }),
        headers: {
          "X-CSRFToken": await getCsrfToken(),
          "Content-Type": "application/json",
        },
      })
      if (ret.ok) {
        const retJson = await ret.json()
        value = retJson.name
      } else {
        alert(`Error uploading file: ${file.name}`)
      }
    })

    reader.readAsDataURL(file)
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
      <input
        type="file"
        name={fieldname}
        on:change={uploadFile}
        accept={ACCEPTED_EXTENSIONS.join(",")}
      />
    </div>

    <button class="btn-outline btn-flat btn-red" on:click|preventDefault={removeFile}>
      {$_("Remove this file")}
    </button>
  </div>
{:else}
  <input
    type="file"
    required={extras.required}
    name={fieldname}
    on:change={uploadFile}
    accept={ACCEPTED_EXTENSIONS.join(",")}
  />
{/if}
<small class="block pt-2 text-gray-500">
  {$_("Supported file types: ")}{ACCEPTED_EXTENSIONS.join(", ")}
</small>
<small class="block text-gray-500">{$_("Maximum file size: 10MB")}</small>

<slot />
