<script lang="ts">
  import { env } from "$env/dynamic/public"

  import EyeSlashIcon from "$components/icons/EyeSlashIcon.svelte"
  import FilePdfIcon from "$components/icons/FilePdfIcon.svelte"

  export let value: string

  export let extras = { notPublic: false }

  const CUTOFF = 30

  $: fileName = value.substring(value.lastIndexOf("/") + 1)
  $: fileExt = fileName.lastIndexOf(".")
</script>

<a
  href="{env.PUBLIC_MEDIA_URL}{value}"
  rel="noreferrer"
  target="_blank"
  class="flex items-center gap-2"
>
  {#if extras.notPublic}
    <EyeSlashIcon />
  {/if}
  <div>
    <FilePdfIcon class="h-4 w-4" />
  </div>
  {fileName.length > CUTOFF
    ? fileName.slice(0, CUTOFF) + "..." + fileName.slice(fileExt)
    : fileName}
</a>
