<script lang="ts">
  import { _ } from "svelte-i18n";
  import { filters, NegotiationStatus } from "$lib/filters";
  import FilterCollapse from "./FilterCollapse.svelte";

  interface Choice {
    state?: boolean;
    value?: NegotiationStatus;
    name?: string;
  }
  interface GroupChoice extends Choice {
    group: string;
    options: { value: NegotiationStatus; name: string }[];
  }
  function isSuperset(set: Set<string>, subset: Set<string>): boolean {
    for (let elem of subset) {
      if (!set.has(elem)) {
        return false;
      }
    }
    return true;
  }

  function hasIntersection(setA: Set<string>, setB: Set<string>): boolean {
    for (let elem of setB) {
      if (setA.has(elem)) return true;
    }
    return false;
  }

  const choices: Array<Choice | GroupChoice> = [
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
  //   mounted() {
  //     this.choices.forEach((choice) => {
  //       if (choice.group) this.toggleSingle(choice as GroupChoice);
  //     });
  //   },
  async function toggleGroup(choice: GroupChoice) {
    // const fieldmap: { [key: string]: string[] } = {
    //   Concluded: ["ORAL_AGREEMENT", "CONTRACT_SIGNED"],
    // };
    const fields = choice.options.map((o) => o.value);
    console.log("FIE", fields);
    console.log(choice.state);

    if (choice.state) {
      $filters.negotiation_status = [...$filters.negotiation_status, ...fields];
    } else {
      $filters.negotiation_status = $filters.negotiation_status.filter(
        (s: string) => !fields.includes(s)
      );
    }
  }
  async function toggleSingle(choice: GroupChoice) {
    const cur_set: Set<string> = new Set($filters.negotiation_status);
    const exp_set: Set<string> = new Set(choice.options.map((o) => o.value));
    const checkbox = document.getElementById(choice.group) as HTMLInputElement;

    if (isSuperset(cur_set, exp_set)) {
      checkbox.indeterminate = false;
      choice.state = true;
    } else if (hasIntersection(cur_set, exp_set)) {
      checkbox.indeterminate = true;
    } else {
      checkbox.indeterminate = false;
      choice.state = false;
    }
  }
</script>

<FilterCollapse
  title={$_("Negotiation status")}
  clearable={$filters.negotiation_status.length > 0}
  on:click={() => ($filters.negotiation_status = [])}
>
  {#each choices as nstat}
    <div>
      {#if nstat.group}
        <div class="custom-control custom-checkbox">
          <label class="custom-control-label orange-checkbox-label font-bold">
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
            <div class="custom-control custom-checkbox">
              <label class="form-check-label custom-control-label">
                <input
                  bind:group={$filters.negotiation_status}
                  class="form-check-input custom-control-input"
                  type="checkbox"
                  value={nstatop.value}
                  on:change={() => toggleSingle(nstat)}
                />
                {$_(nstatop.name)}
              </label>
            </div>
          {/each}
        </div>
      {:else}
        <div class="custom-control custom-checkbox font-weight-bold">
          <input
            id={nstat.value}
            bind:group={$filters.negotiation_status}
            class="form-check-input custom-control-input"
            type="checkbox"
            value={nstat.value}
          />
          <label class="form-check-label custom-control-label" for={nstat.value}>
            {$_(nstat.name)}
          </label>
        </div>
      {/if}
    </div>
  {/each}
</FilterCollapse>
