<script lang="ts">
  import { env } from "$env/dynamic/public"
  import { _ } from "svelte-i18n"
  import type { ChangeEventHandler } from "svelte/elements"

  import { getCsrfToken } from "$lib/utils"

  import { LABEL_CLASS, VALUE_CLASS, WRAPPER_CLASS } from "$components/Fields/consts"
  import Label2 from "$components/Fields/Display2/Label2.svelte"
  import FilePdfIcon from "$components/icons/FilePdfIcon.svelte"

  export let value: string | null
  export let fieldname: string
  export let label = ""
  export let wrapperClass = WRAPPER_CLASS
  export let labelClass = LABEL_CLASS
  export let valueClass = VALUE_CLASS
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

<div class={wrapperClass} data-fieldname={fieldname}>
  {#if label}
    <Label2 value={label} class={labelClass} />
  {/if}
  <div class={valueClass}>
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
          <input type="file" name={fieldname} on:change={uploadFile} {accept} />
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
  </div>
</div>
