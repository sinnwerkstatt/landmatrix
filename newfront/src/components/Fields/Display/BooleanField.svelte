<script lang="ts">
  import { _ } from "svelte-i18n";

  export let value: boolean;
</script>

<div class="boolean_field">
  {#if value}
    {$_("Yes")}
  {:else if value === false}
    {$_("No")}
  {:else}
    NULL
  {/if}
</div>
