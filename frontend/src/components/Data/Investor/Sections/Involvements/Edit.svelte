<script lang="ts">
  import { _ } from "svelte-i18n"

  import { simpleInvestors } from "$lib/stores"
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
  bind:entries={investor.parents}
  createEntry={createInvolvement(tertiary, investor.id)}
  extras={{
    excludeIds: [
      ...investor.parents.map(i => i.parent_investor_id),
      ...investor.children.map(i => i.child_investor_id),
      investor.id,
    ],
  }}
  {filterFn}
  isEmpty={isEmptyInvolvement}
  entryComponent={Entry}
>
  <svelte:fragment slot="extraHeader" let:entry>
    {@const investor = $simpleInvestors.find(
      inv => inv.id === entry.parent_investor_id,
    )}
    {#if investor}
      {#if investor.deleted}
        <span class="text-lg text-red">
          {$_("DELETED")}:
        </span>
      {:else if !investor.active}
        <span class="text-lg text-purple">
          {$_("DRAFT")}:
        </span>
      {/if}
      <span class="text-lg text-pelorous">
        {investor.name} #{investor.id}
      </span>
    {/if}
  </svelte:fragment>
</SubmodelEditField>
