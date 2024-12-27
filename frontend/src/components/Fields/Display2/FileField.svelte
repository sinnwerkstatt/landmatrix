<script lang="ts">
  import { env } from "$env/dynamic/public"

  import EyeSlashIcon from "$components/icons/EyeSlashIcon.svelte"
  import FilePdfIcon from "$components/icons/FilePdfIcon.svelte"

  interface Props {
    value: string
    extras?: { notPublic: boolean }
  }

  let { value, extras = { notPublic: false } }: Props = $props()

  const CUTOFF = 30

  let fileName = $derived(value.substring(value.lastIndexOf("/") + 1))
  let fileExt = $derived(fileName.lastIndexOf("."))
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
  <span class="break-all">
    {fileName.length > CUTOFF
      ? fileName.slice(0, CUTOFF) + "..." + fileName.slice(fileExt)
      : fileName}
  </span>
</a>
