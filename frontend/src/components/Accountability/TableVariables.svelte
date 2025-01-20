<script lang="ts">
  import { onMount } from "svelte"

  import { initTableSelection } from "$lib/accountability/helpers"
  import { tableSelection } from "$lib/accountability/stores"

  import Avatar from "./atomic/Avatar.svelte"
  import BadgeStatus from "./atomic/BadgeStatus.svelte"
  import Checkbox from "./atomic/Checkbox.svelte"
  import Table from "./atomic/Table.svelte"
  import TableCell from "./atomic/TableCell.svelte"
  import TableRow from "./atomic/TableRow.svelte"

  interface Props {
    deal: {
      id: number
      country: { id: number; name: string }
      status: string
      score: {
        status: string
        variables: {
          id: number
          status: string
          score: number | null
          assignee: { id: number; name: string } | null
        }[]
      }
    }
  }

  let { deal }: Props = $props()

  let data = $derived(deal.score.variables ? deal.score.variables : [])

  const columns: { label: string; value: string }[] = [
    { label: "id", value: "id" },
    { label: "variable scoring", value: "variables" },
    { label: "assignee", value: "assignees" },
  ]

  const gridColsTemplate = "32px repeat(3, 1fr)"

  let pageContent = $state([])
  let dealChecked = $state(false)
  let dealPartiallyChecked = $state(false)

  function updateDealCheckbox() {
    if ($tableSelection[deal.id]?.variables) {
      const nvar = Object.keys($tableSelection[deal.id].variables).length
      const nselect = Object.values($tableSelection[deal.id].variables).filter(
        Boolean,
      ).length

      if (nvar == nselect) {
        dealChecked = true
      } else {
        dealChecked = false
        dealPartiallyChecked = nselect > 0
      }
    }
  }

  onMount(() => {
    initTableSelection(deal)
    updateDealCheckbox()
  })

  function checkDeal(value, checked) {
    dealPartiallyChecked = false

    if (checked) {
      deal.score.variables.forEach(v => {
        $tableSelection[deal.id].variables[v.vggt_variable] = true
      })
    } else {
      deal.score.variables.forEach(v => {
        $tableSelection[deal.id].variables[v.vggt_variable] = false
      })
    }
  }

  function removeAssignee() {
    // console.log("Remove assignee")
  }

  $effect(() => {
    updateDealCheckbox($tableSelection[deal.id])
  })

  // $: console.log($tableSelection[deal.id])
</script>

<Table {data} bind:pageContent filters={false} rowHeight="57">
  {#snippet header()}
    <TableRow {gridColsTemplate}>
      <TableCell style="heading">
        <div class="w-fit">
          <Checkbox
            paddingX="0"
            paddingY="0"
            onchanged={checkDeal}
            bind:checked={dealChecked}
            bind:partiallyChecked={dealPartiallyChecked}
          />
        </div>
      </TableCell>

      {#each columns as column (column.value)}
        <TableCell style="heading">{column.label.toUpperCase()}</TableCell>
      {/each}
    </TableRow>
  {/snippet}

  {#snippet body()}
    {#each pageContent as variable (variable.vggt_variable)}
      <TableRow {gridColsTemplate}>
        <TableCell>
          <div class="w-fit">
            <Checkbox
              paddingX="0"
              paddingY="0"
              value={variable.vggt_variable}
              bind:checked={$tableSelection[deal.id].variables[variable.vggt_variable]}
            />
          </div>
        </TableCell>

        <TableCell>{variable.vggt_variable}</TableCell>

        <TableCell>
          <BadgeStatus type="dot" value={variable.status} />
        </TableCell>

        <TableCell>
          {#if variable.assignee}
            <Avatar
              size="sm"
              label={variable.assignee?.name}
              initials={variable.assignee?.initials}
              buttonOnHover={true}
              on:click={removeAssignee}
            />
          {/if}
        </TableCell>
      </TableRow>
    {/each}
  {/snippet}
</Table>
