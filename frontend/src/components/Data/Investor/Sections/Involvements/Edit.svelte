<script lang="ts">
  import { _ } from "svelte-i18n"

  import { InvolvementRole, type InvestorHull, type Involvement } from "$lib/types/data"

  import SubmodelEditField from "$components/Fields/SubmodelEditField.svelte"

  import Entry from "./Entry.svelte"
  import { createInvolvement, isEmptyInvolvement } from "./involvements"

  export let investor: InvestorHull
  export let tertiary = false

  $: label = tertiary ? $_("Tertiary investor/lender") : $_("Parent company")

  $: filterFn = (involvement: Involvement) =>
    involvement.child_investor_id === investor.id &&
    involvement.role === (tertiary ? InvolvementRole.LENDER : InvolvementRole.PARENT)
</script>

<SubmodelEditField
  {label}
  bind:entries={investor.involvements}
  createEntry={createInvolvement(tertiary, investor.id)}
  entryIdKey="id"
  extras={{}}
  {filterFn}
  isEmpty={isEmptyInvolvement}
  entryComponent={Entry}
/>
