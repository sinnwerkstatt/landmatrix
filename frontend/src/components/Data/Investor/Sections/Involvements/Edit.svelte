<script lang="ts">
  import { _ } from "svelte-i18n"

  import { simpleInvestors } from "$lib/stores"
  import {
    InvolvementRole,
    type Involvement,
    type MutableInvestorHull,
  } from "$lib/types/data"

  import SubmodelEditField from "$components/Fields/SubmodelEditField.svelte"

  import Entry from "./Entry.svelte"
  import { createInvolvement, isEmptyInvolvement } from "./involvements"

  interface Props {
    investor: MutableInvestorHull
    tertiary?: boolean
  }

  let { investor = $bindable(), tertiary = false }: Props = $props()

  let label = $derived(tertiary ? $_("Tertiary investor/lender") : $_("Parent company"))

  let filterFn = (involvement: Involvement) =>
    involvement.child_investor_id === investor.id &&
    involvement.role === (tertiary ? InvolvementRole.LENDER : InvolvementRole.PARENT)

  // Note: Involvements are parents by definition!
  let involvements = $state(investor.selected_version.involvements)

  const onchange = () => {
    investor.selected_version.involvements = involvements
  }
</script>

<SubmodelEditField
  model="investor"
  fieldname="involvements"
  {label}
  bind:entries={involvements}
  createEntry={createInvolvement(tertiary, investor.id)}
  extras={{
    excludeIds: [
      ...involvements.map(i => i.parent_investor_id),
      ...investor.children.map(i => i.child_investor_id),
      investor.id,
    ],
  }}
  {filterFn}
  isEmpty={isEmptyInvolvement}
  entryComponent={Entry}
  {onchange}
>
  {#snippet extraHeader(entry)}
    {@const investor = $simpleInvestors.find(
      inv => inv.id === entry.parent_investor_id,
    )}
    {#if investor}
      {#if investor.deleted}
        <span class="text-red">
          {$_("Deleted")}:
        </span>
      {:else if !investor.active}
        <span class="text-purple">
          {$_("Draft")}:
        </span>
      {/if}
      <span class="font-bold text-pelorous">
        {investor.name} #{investor.id}
      </span>
    {/if}
  {/snippet}
</SubmodelEditField>
