<script lang="ts">
  import { _ } from "svelte-i18n"

  import { dealChoices } from "$lib/fieldChoices"
  import { filters } from "$lib/filters"
  import type { NegotiationStatus, NegotiationStatusGroup } from "$lib/types/data"

  import ContextHelper from "$components/ContextHelper.svelte"

  import FilterCollapse from "./FilterCollapse.svelte"

  let negotiationStatus = $derived($dealChoices.negotiation_status)
  let negotiationStatusGroups = $derived($dealChoices.negotiation_status_group)

  const checkGroupCheckboxes = () =>
    negotiationStatusGroups.map(x => x.value).forEach(setGroupCheckboxState)

  function isSuperset(set: Set<string>, subset: Set<string>): boolean {
    for (let elem of subset) if (!set.has(elem)) return false
    return true
  }

  function hasIntersection(setA: Set<string>, setB: Set<string>): boolean {
    for (let elem of setB) if (setA.has(elem)) return true
    return false
  }

  function setGroupCheckboxState(group: string | NegotiationStatusGroup) {
    const checkbox = document.getElementById(group) as HTMLInputElement
    if (!checkbox) return

    const cur_set: Set<string> = new Set($filters.negotiation_status)
    const exp_set: Set<string> = new Set(
      negotiationStatus.filter(x => x.group === group).map(x => x.value),
    )

    if (isSuperset(cur_set, exp_set)) {
      checkbox.indeterminate = false
      checkbox.checked = true
    } else if (hasIntersection(cur_set, exp_set)) {
      checkbox.indeterminate = true
    } else {
      checkbox.indeterminate = false
      checkbox.checked = false
    }
  }

  function toggleGroup(group: string | NegotiationStatusGroup, e: Event) {
    const checked = (e.target as HTMLInputElement).checked

    const groupValues = negotiationStatus
      .filter(x => x.group === group)
      .map(x => x.value) as NegotiationStatus[]

    $filters.negotiation_status = checked
      ? [...$filters.negotiation_status, ...groupValues]
      : $filters.negotiation_status.filter(s => !groupValues.includes(s))
  }
</script>

<FilterCollapse
  clearable={$filters.negotiation_status.length > 0}
  onclear={() => ($filters.negotiation_status = [])}
  onExpanded={checkGroupCheckboxes}
  title={$_("Negotiation status")}
>
  {#each negotiationStatusGroups as { value: group, label: groupLabel }}
    {@const groupNegotiationStatus = negotiationStatus.filter(x => x.group === group)}

    <label class="block font-bold">
      <input id={group} type="checkbox" onchange={e => toggleGroup(group, e)} />
      {groupLabel}
    </label>

    {#each groupNegotiationStatus as { value, label }}
      <label class="block pl-4">
        <input
          bind:group={$filters.negotiation_status}
          type="checkbox"
          {value}
          onchange={() => setGroupCheckboxState(group)}
        />
        {label}
      </label>
    {/each}
  {/each}

  <div class="text-right">
    <ContextHelper identifier="filterbar_negotiation_status" class="mt-2 size-5" />
  </div>
</FilterCollapse>
