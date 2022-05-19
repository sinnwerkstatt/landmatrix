<script lang="ts">
  import Select from "svelte-select";
  import MinusIcon from "$components/icons/MinusIcon.svelte";
  import PlusIcon from "$components/icons/PlusIcon.svelte";
  import type { FormField } from "../fields";
  import LowLevelDateYearField from "./LowLevelDateYearField.svelte";

  export let formfield: FormField;
  export let value;
  let current = -1;

  $: vals = JSON.stringify(value);
  //   computed: {
  //     filteredVals() {
  //       return this.vals.filter((x) => x.date || x.choice);
  //     },
  //   },

  function updateEntries() {
    // value = value.map((v, i) => {
    //   let current = i === this.current ? { current: true } : {};
    //   delete v.current;
    //   return { ...v, ...current };
    // });
    // this.$emit("input", this.filteredVals);
  }
  function updateCurrent(i) {
    current = i;
    updateEntries();
  }
  function addEntry() {
    value = [...value, []];
    updateEntries();
  }
  function removeEntry(index) {
    if (current === value.length - 1) this.current = null;
    value.splice(index, 1);
    updateEntries();
  }
</script>

<div class="json_date_choice_field whitespace-nowrap">
  <table class="w-full">
    <thead>
      <tr>
        <th>Current</th>
        <th>Date</th>
        <th>Choice</th>
        <th />
      </tr>
    </thead>
    <tbody>
      {#each value as val, i}
        <tr class:is-current={val.current}>
          <td class="text-center p-1" on:click={() => updateCurrent(i)}>
            <div class="form-check form-check-inline">
              <input
                required={value.length > 0 && (value[0].date || value[0].choice)}
                type="checkbox"
                bind:checked={val.current}
              />
            </div>
          </td>
          <td class="w-36 p-1">
            <LowLevelDateYearField
              bind:value={val.date}
              required={formfield.required}
              on:input={updateEntries}
            />
          </td>
          <td class="w-2/3 p-1">
            <Select
              items={Object.entries(formfield.choices).map(([value, label]) => ({
                value,
                label,
              }))}
              value={val.choice}
              showChevron
            />
            <!--              @input="updateEntries"-->
          </td>

          <td class="buttons p-1">
            <button type="button" on:click={addEntry}
              ><PlusIcon class="w-5 h-5" /></button
            >
            <button
              type="button"
              disabled={value.length <= 1}
              on:click={() => removeEntry(i)}><MinusIcon class="w-5 h-5" /></button
            >
          </td>
        </tr>
      {/each}
    </tbody>
  </table>
</div>
