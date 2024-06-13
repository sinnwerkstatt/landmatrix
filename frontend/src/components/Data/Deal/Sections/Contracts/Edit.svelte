<script lang="ts">
  import { _ } from "svelte-i18n"

  import { type Contract, type DealHull } from "$lib/types/newtypes"

  import SubmodelEditField from "$components/Fields/SubmodelEditField.svelte"

  import Entry from "./Entry.svelte"

  export let deal: DealHull

  const createContract = (nid: string): Contract => ({
    id: null!,
    dealversion: null!,
    nid,
    number: "",
    date: null,
    expiration_date: null,
    agreement_duration: null,
    comment: "",
  })
</script>

<SubmodelEditField
  label={$_("Contract")}
  bind:entries={deal.selected_version.contracts}
  createEntry={createContract}
  entryComponent={Entry}
/>
