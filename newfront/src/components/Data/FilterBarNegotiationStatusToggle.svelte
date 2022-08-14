<script lang="ts">
  import { _ } from "svelte-i18n";
  import { filters } from "$lib/filters";
  import { NegotiationStatus } from "$lib/types/deal";
  import FilterCollapse from "./FilterCollapse.svelte";

  interface Choice {
    value?: NegotiationStatus;
    name?: string;
  }
  interface GroupChoice extends Choice {
    group: string;
    state: boolean;
    options: { value: NegotiationStatus; name: string }[];
  }

  function isSuperset(set: Set<string>, subset: Set<string>): boolean {
    for (let elem of subset) if (!set.has(elem)) return false;
    return true;
  }
  function hasIntersection(setA: Set<string>, setB: Set<string>): boolean {
    for (let elem of setB) if (setA.has(elem)) return true;
    return false;
  }

  // const choices: Array<Choice | GroupChoice> = [
  const choices = [
    {
      group: "Intended",
      state: undefined,
      options: [
        {
          value: NegotiationStatus.EXPRESSION_OF_INTEREST,
          name: "Expression of interest",
        },
        { value: NegotiationStatus.UNDER_NEGOTIATION, name: "Under negotiation" },
        {
          value: NegotiationStatus.MEMORANDUM_OF_UNDERSTANDING,
          name: "Memorandum of understanding",
        },
      ],
    },
    {
      group: "Concluded",
      state: undefined,
      options: [
        { value: NegotiationStatus.ORAL_AGREEMENT, name: "Oral agreement" },
        { value: NegotiationStatus.CONTRACT_SIGNED, name: "Contract signed" },
        { value: NegotiationStatus.CHANGE_OF_OWNERSHIP, name: "Change of ownership" },
      ],
    },
    {
      group: "Failed",
      state: undefined,
      options: [
        { value: NegotiationStatus.NEGOTIATIONS_FAILED, name: "Negotiations failed" },
        { value: NegotiationStatus.CONTRACT_CANCELED, name: "Contract cancelled" },
      ],
    },
    { value: NegotiationStatus.CONTRACT_EXPIRED, name: "Contract expired" },
  ];

  //   watch: {
  //     "$store.state.signalNegstat"() {
  //       this.choices.forEach((choice) => {
  //         if (choice.group) this.toggleSingle(choice as GroupChoice);
  //       });
  //     },
  //   },

  // const isGroupChoice = (c): c is GroupChoice => !!c?.group;
  // onMount(() => {
  //   choices.forEach((choice) => {
  //     if (isGroupChoice(choice)) toggleSingle(choice);
  //   });
  // });

  async function toggleGroup(choice: GroupChoice) {
    // const fieldmap: { [key: string]: string[] } = {
    //   Concluded: ["ORAL_AGREEMENT", "CONTRACT_SIGNED"],
    // };
    const fields = choice.options.map((o) => o.value);

    if (choice.state) {
      $filters.negotiation_status = [...$filters.negotiation_status, ...fields];
    } else {
      $filters.negotiation_status = $filters.negotiation_status.filter(
        (s: NegotiationStatus) => !fields.includes(s)
      );
    }
  }
  async function toggleSingle(choice: GroupChoice) {
    const cur_set: Set<string> = new Set($filters.negotiation_status);
    const exp_set: Set<string> = new Set(choice.options.map((o) => o.value));
    const checkbox = document.getElementById(choice.group) as HTMLInputElement;

    if (isSuperset(cur_set, exp_set)) {
      checkbox.indeterminate = false;
      // choice.state = true;
      checkbox.checked = true;
    } else if (hasIntersection(cur_set, exp_set)) {
      checkbox.indeterminate = true;
    } else {
      checkbox.indeterminate = false;
      // choice.state = false;
      checkbox.checked = false;
    }
  }
</script>

<FilterCollapse
  title={$_("Negotiation status")}
  clearable={$filters.negotiation_status.length > 0}
  on:click={() => ($filters.negotiation_status = [])}
>
  {#each choices as nstat}
    {#if nstat.group}
      <label class="font-bold block">
        <input
          id={nstat.group}
          bind:checked={nstat.state}
          class="custom-control-input"
          type="checkbox"
          on:change={() => toggleGroup(nstat)}
        />
        {$_(nstat.group)}
      </label>
      {#each nstat.options as nstatop}
        <label class="block pl-4">
          <input
            bind:group={$filters.negotiation_status}
            class="form-check-input custom-control-input"
            type="checkbox"
            value={nstatop.value}
            on:change={() => toggleSingle(nstat)}
          />
          {$_(nstatop.name)}
        </label>
      {/each}
    {:else}
      <label class="font-bold block">
        <input
          bind:group={$filters.negotiation_status}
          type="checkbox"
          value={nstat.value}
        />
        {$_(nstat.name)}
      </label>
    {/if}
  {/each}
</FilterCollapse>
