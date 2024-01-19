<script lang="ts">
  import { _ } from "svelte-i18n"

  export let value: string

  export let extras = { url: false, ocid: false, email: false }
</script>

{#if extras.url}
  <a href={value} target="_blank" rel="noreferrer">{new URL(value).hostname}</a>
  <!-- TODO handle extras.email -->
{:else if extras.ocid}
  <a
    href="https://www.openlandcontracts.org/contract/{value}/view#/pdf"
    target="_blank"
    rel="noreferrer"
  >
    {$_("Access more information about this contract on OpenLandContracts.org")}
  </a>
{:else}
  {value ?? "—"}
{/if}
