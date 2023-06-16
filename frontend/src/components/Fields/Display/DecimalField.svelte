<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { FormField } from "$components/Fields/fields"

  export let formfield: FormField
  export let value: number
</script>

<div class="flex items-center">
  {value?.toLocaleString("fr") ?? "—"}
  {#if value && formfield.unit}
    {$_(formfield.unit)}
  {/if}
</div>
