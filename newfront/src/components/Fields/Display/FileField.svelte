<script lang="ts">
  import type { FormField } from "$components/Fields/fields";
  import FilePdfIcon from "$components/icons/FilePdfIcon.svelte";
  import EyeSlashIcon from "$components/icons/EyeSlashIcon.svelte";

  export let formfield: FormField;
  export let value: string;
  export let model: string;
  export let fileNotPublic = false;
</script>

<div class="file_field">
  <a href="{import.meta.env.VITE_MEDIA_URL}{value}" target="_blank">
    {#if fileNotPublic}
      <EyeSlashIcon />
    {/if}
    <FilePdfIcon />
    {value.replace("uploads/", "")}
  </a>
</div>
