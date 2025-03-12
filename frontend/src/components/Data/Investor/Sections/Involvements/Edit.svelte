<script lang="ts">
  import { _ } from "svelte-i18n"

  import { simpleInvestors } from "$lib/stores"
  import { InvolvementRole, type MutableInvestorHull } from "$lib/types/data"

  import SubmodelEditField from "$components/Fields/SubmodelEditField.svelte"

  import Entry from "./Entry.svelte"
  import { createInvolvement, isEmptyInvolvement } from "./involvements"

  interface Props {
    investor: MutableInvestorHull
    tertiary?: boolean
  }

  let { investor = $bindable(), tertiary = false }: Props = $props()

  const label = $derived(
    tertiary ? $_("Tertiary investor/lender") : $_("Parent company"),
  )
  const involvements = $derived(investor.selected_version.involvements)
  const parents = $derived(involvements.filter(i => i.role === InvolvementRole.PARENT))
  const lender = $derived(involvements.filter(i => i.role === InvolvementRole.LENDER))

  let entries = $state(
    investor.selected_version.involvements.filter(
      i => i.role === (tertiary ? InvolvementRole.LENDER : InvolvementRole.PARENT),
    ),
  )

  const onchange = () => {
    investor.selected_version.involvements = tertiary
      ? [...parents, ...entries]
      : [...lender, ...entries]
  }
</script>

<SubmodelEditField
  model="investor"
  fieldname="involvements"
  {label}
  bind:entries
  createEntry={createInvolvement(tertiary, investor.id)}
  extras={{
    excludeIds: [
      ...involvements.map(i => i.parent_investor_id),
      ...investor.children.map(i => i.child_investor_id),
      investor.id,
    ],
  }}
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
