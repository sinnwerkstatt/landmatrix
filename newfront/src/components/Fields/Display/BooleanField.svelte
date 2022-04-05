<script lang="ts">
  import type { FormField } from "$components/Fields/fields";
  import { _ } from "svelte-i18n";

  export let formfield: FormField;
  export let value: boolean;
  export let model: string;
</script>

<div class="boolean_field">
  {#if value}
    {$_("Yes")}
  {:else if value === false}
    {$_("No")}
  {:else}NULL
  {/if}
</div>
