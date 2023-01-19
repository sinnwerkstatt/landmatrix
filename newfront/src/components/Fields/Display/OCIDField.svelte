<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { FormField } from "$components/Fields/fields"

  export let formfield: FormField
  export let value: string
</script>

<div class="ocid_field" data-name={formfield?.name ?? ""}>
  {#if value}
    {value}
    <a
      href="https://www.openlandcontracts.org/contract/{value}/view#/pdf"
      target="_blank"
      rel="noreferrer"
    >
      {$_("Access more information about this contract on OpenLandContracts.org")}
    </a>
  {:else}
    —
  {/if}
</div>
