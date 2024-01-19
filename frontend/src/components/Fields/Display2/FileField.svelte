<script lang="ts">
  import EyeSlashIcon from "$components/icons/EyeSlashIcon.svelte"
  import FilePdfIcon from "$components/icons/FilePdfIcon.svelte"

  export let value: string

  export let extras = { notPublic: false }

  $: fileName = value.substring(value.lastIndexOf("/") + 1)
</script>

<a href={value} rel="noreferrer" target="_blank">
  {#if extras.notPublic}
    <EyeSlashIcon />
  {/if}
  <FilePdfIcon />
  {fileName}
</a>
