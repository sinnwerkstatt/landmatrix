<script lang="ts">
  import { _ } from "svelte-i18n"

  import { filters } from "$lib/filters"
  import { NegotiationStatus } from "$lib/types/deal"

  import FilterCollapse from "./FilterCollapse.svelte"

  interface Choice {
    value: NegotiationStatus
    name: string
  }

  interface GroupChoice {
    group: string
    options: Choice[]
  }

  function isSuperset(set: Set<string>, subset: Set<string>): boolean {
    for (let elem of subset) if (!set.has(elem)) return false
    return true
  }

  function hasIntersection(setA: Set<string>, setB: Set<string>): boolean {
    for (let elem of setB) if (setA.has(elem)) return true
    return false
  }

  let choices: Array<GroupChoice | Choice>
  $: choices = [
    {
      group: $_("Intended"),
      options: [
        {
          value: NegotiationStatus.EXPRESSION_OF_INTEREST,
          name: $_("Expression of interest"),
        },
        {
          value: NegotiationStatus.UNDER_NEGOTIATION,
          name: $_("Under negotiation"),
        },
        {
          value: NegotiationStatus.MEMORANDUM_OF_UNDERSTANDING,
          name: $_("Memorandum of understanding"),
        },
      ],
    },
    {
      group: $_("Concluded"),
      options: [
        {
          value: NegotiationStatus.ORAL_AGREEMENT,
          name: $_("Oral agreement"),
        },
        {
          value: NegotiationStatus.CONTRACT_SIGNED,
          name: $_("Contract signed"),
        },
        {
          value: NegotiationStatus.CHANGE_OF_OWNERSHIP,
          name: $_("Change of ownership"),
        },
      ],
    },
    {
      group: $_("Failed"),
      options: [
        {
          value: NegotiationStatus.NEGOTIATIONS_FAILED,
          name: $_("Negotiations failed"),
        },
        {
          value: NegotiationStatus.CONTRACT_CANCELED,
          name: $_("Contract cancelled"),
        },
      ],
    },
    {
      value: NegotiationStatus.CONTRACT_EXPIRED,
      name: $_("Contract expired"),
    },
  ]

  const isGroupChoice = (c: Choice | GroupChoice): c is GroupChoice =>
    Object.prototype.hasOwnProperty.call(c, "group")

  const checkGroups = () => {
    choices.forEach(choice => {
      if (isGroupChoice(choice)) {
        toggleSingle(choice)
        return true
      }
      return false
    })
  }

  function toggleGroup(choice: GroupChoice, e: Event) {
    const checked = (e.target as HTMLInputElement).checked
    const fields = choice.options.map(o => o.value)

    $filters.negotiation_status = checked
      ? [...$filters.negotiation_status, ...fields]
      : $filters.negotiation_status.filter(s => !fields.includes(s))
  }

  function toggleSingle(choice: GroupChoice) {
    const cur_set: Set<string> = new Set($filters.negotiation_status)
    const exp_set: Set<string> = new Set(choice.options.map(o => o.value))
    const checkbox = document.getElementById(choice.group) as HTMLInputElement

    if (!checkbox) return
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
</script>

<FilterCollapse
  clearable={$filters.negotiation_status.length > 0}
  on:clear={() => ($filters.negotiation_status = [])}
  on:expanded={checkGroups}
  title={$_("Negotiation status")}
>
  {#each choices as nstat}
    {#if isGroupChoice(nstat)}
      <label class="block font-bold">
        <input
          id={nstat.group}
          type="checkbox"
          on:change={e => toggleGroup(nstat, e)}
        />
        {nstat.group}
      </label>
      {#each nstat.options as nstatop}
        <label class="block pl-4">
          <input
            bind:group={$filters.negotiation_status}
            type="checkbox"
            value={nstatop.value}
            on:change={() => toggleSingle(nstat)}
          />
          {nstatop.name}
        </label>
      {/each}
    {:else}
      <label class="block font-bold">
        <input
          bind:group={$filters.negotiation_status}
          type="checkbox"
          value={nstat.value}
        />
        {nstat.name}
      </label>
    {/if}
  {/each}
</FilterCollapse>
