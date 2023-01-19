<script lang="ts">
  import type { FormField } from "$components/Fields/fields"
  import EyeSlashIcon from "$components/icons/EyeSlashIcon.svelte"
  import FilePdfIcon from "$components/icons/FilePdfIcon.svelte"

  export let value: string
  export let formfield: FormField
  export let fileNotPublic = false
</script>

<div class="file_field" data-name={formfield?.name ?? ""}>
  {#if value}
    <a href="{import.meta.env.VITE_MEDIA_URL}{value}" target="_blank">
      {#if fileNotPublic}
        <EyeSlashIcon />
      {/if}
      <FilePdfIcon />
      {value.replace("uploads/", "")}
    </a>
  {:else}
    —
  {/if}
</div>
