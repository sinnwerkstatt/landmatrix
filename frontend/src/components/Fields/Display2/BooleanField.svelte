<script lang="ts">
  import { _ } from "svelte-i18n"

  export let value: boolean | null
</script>

{#if value === true}
  {$_("Yes")}
{:else if value === false}
  {$_("No")}
{:else}
  —
{/if}
