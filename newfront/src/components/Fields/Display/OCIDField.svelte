<script lang="ts">
  import { _ } from "svelte-i18n";
  import type { FormField } from "$components/Fields/fields";

  export let formfield: FormField;
  export let value: string;
  export let model: string;

  //$: ocidUrl = `https://www.openlandcontracts.org/contract/${value}/view#/pdf`;
</script>

<div class="ocid_field">
  <div>{value}</div>
  <div>
    <a
      href="https://www.openlandcontracts.org/contract/{value}/view#/pdf"
      target="_blank"
    >
      {$_("Access more information about this contract on OpenLandContracts.org")}</a
    >
  </div>
</div>
