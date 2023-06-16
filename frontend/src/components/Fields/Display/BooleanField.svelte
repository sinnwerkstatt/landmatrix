<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { FormField } from "$components/Fields/fields"

  export let value: boolean
  export let formfield: FormField
</script>

{#if value}
  {$_("Yes")}
{:else if value === false}
  {$_("No")}
{:else}
  —
{/if}
