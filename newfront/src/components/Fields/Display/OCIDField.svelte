<script lang="ts">
  import { _ } from "svelte-i18n";

  export let value: string;
</script>

<div class="ocid_field">
  {#if value}
    {value}
    <a
      href="https://www.openlandcontracts.org/contract/{value}/view#/pdf"
      target="_blank"
    >
      {$_("Access more information about this contract on OpenLandContracts.org")}</a
    >
  {:else}
    —
  {/if}
</div>
