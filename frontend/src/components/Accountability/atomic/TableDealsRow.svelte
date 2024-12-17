<script lang="ts">
  import { onMount } from "svelte"
  import { slide } from "svelte/transition"

  // import { page } from "$app/stores"

  import { initTableSelection, unique } from "$lib/accountability/helpers"
  import { bulkUpdateDealVariable } from "$lib/accountability/scores"
  import {
    currentDeal,
    currentVariable,
    deals,
    openDrawer,
    tableSelection,
    tableSelectionChecked,
    users,
  } from "$lib/accountability/stores"

  import IconChevron from "../icons/IconChevron.svelte"
  import Modal from "../Modal.svelte"
  import Avatar from "./Avatar.svelte"
  import AvatarGroup from "./AvatarGroup.svelte"
  import BadgeStatus from "./BadgeStatus.svelte"
  import Checkbox from "./Checkbox.svelte"
  import InputAssignee from "./InputAssignee.svelte"
  import TableCell from "./TableCell.svelte"
  import TableRow from "./TableRow.svelte"
  import VariableDots from "./VariableDots.svelte"

  export let gridColsTemplate = ""
  export let columns = []
  export let deal

  let dealChecked = false
  let dealPartiallyChecked = false
  let open = false
  let openBulkUpdateModal = false

  let bulkUpdateInfo = {
    toUpdate: [],
    assignee: null,
  }

  function updateDealCheckbox() {
    if (!$tableSelection[deal.id]?.variables) {
      dealChecked = false
      dealPartiallyChecked = false
    } else {
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

  // ==================================================================================================
  // More checkbox reactivity functions
  function checkDeal(event) {
    const checked = event.detail.checked

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

  $: updateDealCheckbox($tableSelection[deal.id])

  // ==================================================================================================
  // Assignment functions
  function getDealAssignees(deal) {
    const assigneesID = unique(deal.score.variables.map(v => v.assignee).filter(Number))
    let assignees = []
    assigneesID.forEach(id => {
      const assignee = $users.find(u => u.id == id)
      assignees.push(assignee)
    })
    return assignees
  }

  $: dealAssignees = getDealAssignees(deal) ?? []

  async function selectAssignee(event, vggt_variable) {
    const assigneeID = event.detail.assignee

    if ($tableSelectionChecked.length == 0) {
      bulkUpdateInfo = {
        toUpdate: [{ deal: deal.id, variable: vggt_variable }],
        assignee: assigneeID,
      }
      await updateAssignee()
    } else {
      // Add clicked variable to toUpdate even if it wasn't selected
      let toUpdate = $tableSelectionChecked
      if (!toUpdate.find(e => e.deal == deal.id && e.variable == vggt_variable)) {
        toUpdate.push({ deal: `${deal.id}`, variable: `${vggt_variable}` })
      }

      bulkUpdateInfo = { toUpdate, assignee: assigneeID }
      openBulkUpdateModal = true
    }
  }

  async function unselectAssignee(vggt_variable) {
    if ($tableSelectionChecked.length == 0) {
      bulkUpdateInfo = {
        toUpdate: [{ deal: deal.id, variable: vggt_variable }],
        assignee: null,
      }
      await updateAssignee()
    } else {
      let toUpdate = $tableSelectionChecked
      if (!toUpdate.find(e => e.deal == deal.id && e.variable == vggt_variable)) {
        toUpdate.push({ deal: `${deal.id}`, variable: `${vggt_variable}` })
      }

      bulkUpdateInfo = { toUpdate, assignee: null }
      openBulkUpdateModal = true
    }
  }

  async function updateAssignee() {
    try {
      const res = await bulkUpdateDealVariable(bulkUpdateInfo)
      if (res.ok) {
        // Update $deals (so we dont' fetch all deals again -> performance)
        bulkUpdateInfo.toUpdate.forEach(e => {
          const deal_index = $deals.findIndex(d => d.id == e.deal)
          const variable_index = $deals
            .find(d => d.id == e.deal)
            .score.variables.findIndex(v => v.vggt_variable == e.variable)

          $deals[deal_index].score.variables[variable_index].assignee =
            bulkUpdateInfo.assignee
        })
      }
    } catch (error) {
      console.error(error)
      console.error(error.body.message)
    }
    bulkUpdateInfo = { toUpdate: [], assignee: null }
    openBulkUpdateModal = false
  }

  // ==================================================================================================
  // Opening a deal page or a scoring drawer
  function openVariable(id) {
    currentDeal.set(deal.id)
    currentVariable.set(id)
    openDrawer.set(true)
  }
</script>

<div class="row">
  <!-- Deal row -->
  <TableRow {gridColsTemplate}>
    <TableCell>
      <div class="flex items-center gap-2">
        <Checkbox
          paddingX="0"
          paddingY="0"
          value={deal.id}
          bind:partiallyChecked={dealPartiallyChecked}
          bind:checked={dealChecked}
          on:changed={checkDeal}
        />
        <button
          class="text-a-gray-400 {!open ? 'rotate-180' : ''} "
          on:click={() => (open = !open)}
        >
          <IconChevron size="16" />
        </button>
      </div>
    </TableCell>

    {#each columns as column}
      <!-- {@const val = deal[column.value]} -->

      <!-- Deal ID -->
      {#if column.value == "id"}
        <TableCell>
          <!-- <a class="link" href="{$page.url.href}{deal.id}/">Deal #{deal.id}</a> -->

          <!-- TMP: Click on deal opens variables instead of deal page -->
          <button class="text-left" on:click={() => (open = !open)}>
            Deal #{deal.id}
          </button>

          <!-- TODO: New label for new version -->
        </TableCell>

        <!-- Deal Status -->
      {:else if column.value == "status"}
        <TableCell>
          <BadgeStatus value={deal.score.status} />
        </TableCell>

        <!-- Variable Scoring -->
      {:else if column.value == "variables"}
        <TableCell>
          <VariableDots variables={deal.score.variables} />
        </TableCell>

        <!-- Assignee -->
      {:else if column.value == "assignees"}
        <TableCell>
          {#if dealAssignees && dealAssignees.length == 1}
            <Avatar
              size="sm"
              label={dealAssignees[0].name}
              initials={dealAssignees[0].initials}
            />
          {:else if dealAssignees && dealAssignees.length > 1}
            <AvatarGroup size="sm" users={dealAssignees} maxAvatars="4" />
          {/if}
        </TableCell>

        <!-- Else (simple text) -->
      {:else if column.value == "country"}
        <TableCell>{deal?.country?.name}</TableCell>
      {/if}
    {/each}
  </TableRow>

  <!-- Variable rows -->
  {#if open}
    <div transition:slide>
      <TableRow {gridColsTemplate}>
        {#each deal.score.variables as variable}
          <TableCell style="nested">
            <span class="w-fit">
              <Checkbox
                paddingX="0"
                paddingY="0"
                value={variable.vggt_variable}
                bind:checked={$tableSelection[deal.id].variables[
                  variable.vggt_variable
                ]}
              />
            </span>
          </TableCell>

          <TableCell style="nested">
            <button
              class="w-fit text-left underline underline-offset-4"
              on:click={() => openVariable(variable.vggt_variable)}
            >
              Variable {variable.vggt_variable}
            </button>
          </TableCell>
          <TableCell style="nested"></TableCell>

          <TableCell style="nested">
            <BadgeStatus type="dot" value={variable.status} />
          </TableCell>

          <TableCell style="nested">
            <InputAssignee
              auto={false}
              size="sm"
              extraClass=""
              showOnHover={true}
              assigneeID={variable.assignee}
              on:selectAssignee={event => selectAssignee(event, variable.vggt_variable)}
              on:unselectAssignee={() => unselectAssignee(variable.vggt_variable)}
            />
          </TableCell>

          <TableCell style="nested"></TableCell>
        {/each}
      </TableRow>
    </div>
  {/if}
</div>

<Modal
  bind:open={openBulkUpdateModal}
  title="Confirm assignment"
  on:click={updateAssignee}
>
  <p>
    Are you sure you want to reassign all selected variables? This action cannot be
    undone.
  </p>
  <p>
    This change will affect {bulkUpdateInfo.toUpdate.length} variables from {unique(
      bulkUpdateInfo.toUpdate.map(e => e.deal),
    ).length} deals.
  </p>
</Modal>
