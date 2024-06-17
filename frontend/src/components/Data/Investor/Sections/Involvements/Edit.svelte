<script lang="ts">
  import { _ } from "svelte-i18n"

  import { type InvestorHull, type Involvement } from "$lib/types/data"
  import { isEmptySubmodel } from "$lib/utils/data_processing"

  import Entry from "$components/Data/DataSources/Entry.svelte"
  import SubmodelEditField from "$components/Fields/SubmodelEditField.svelte"

  export let investor: InvestorHull
  export let tertiary = false

  $: label = tertiary ? $_("Tertiary investor/lender") : $_("Parent company")

  enum Role {
    PARENT = "PARENT",
    LENDER = "LENDER",
  }

  const createInvolvement = (id: string): Involvement => ({
    // weird id nid confusion
    id: id,
    parent_investor_id: null!,
    child_investor_id: investor.id,
    role: tertiary ? Role.LENDER : Role.PARENT,
    loans_currency_id: null,
    investment_type: [],
    percentage: null,
    loans_amount: null,
    loans_date: null,
    parent_relation: null,
    comment: "",
  })

  $: filterFn = (involvement: Involvement) =>
    involvement.child_investor_id === investor.id &&
    involvement.role === (tertiary ? Role.LENDER : Role.PARENT)

  $: isEmpty = (involvement: Involvement) =>
    isEmptySubmodel(involvement, ["id", "role", "child_investor_id", "file_not_public"])
</script>

<SubmodelEditField
  {label}
  bind:entries={investor.involvements}
  createEntry={createInvolvement}
  entryIdKey="id"
  extras={{}}
  {filterFn}
  {isEmpty}
  entryComponent={Entry}
/>
