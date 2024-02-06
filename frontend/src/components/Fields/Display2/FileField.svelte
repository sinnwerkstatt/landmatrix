<script lang="ts">
  import { env } from "$env/dynamic/public"

  import EyeSlashIcon from "$components/icons/EyeSlashIcon.svelte"
  import FilePdfIcon from "$components/icons/FilePdfIcon.svelte"

  export let value: string

  export let extras = { notPublic: false }

  $: fileName = value.substring(value.lastIndexOf("/") + 1)
</script>

<a href="{env.PUBLIC_MEDIA_URL}{value}" rel="noreferrer" target="_blank">
  {#if extras.notPublic}
    <EyeSlashIcon />
  {/if}
  <FilePdfIcon />
  {fileName}
</a>
