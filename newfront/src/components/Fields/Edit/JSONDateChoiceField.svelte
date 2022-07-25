<script lang="ts">
  import { _ } from "svelte-i18n";
  import MinusIcon from "$components/icons/MinusIcon.svelte";
  import PlusIcon from "$components/icons/PlusIcon.svelte";
  import type { FormField } from "../fields";
  import LowLevelDateYearField from "./LowLevelDateYearField.svelte";
  import TypedChoiceField from "./TypedChoiceField.svelte";

  interface JSONDateChoiceField {
    date?: string;
    choice?: string;
    current?: boolean;
  }

  export let formfield: FormField;
  export let value;

  let valueCopy: JSONDateChoiceField[] = JSON.parse(JSON.stringify(value ?? [{}]));

  $: filteredValueCopy = valueCopy.filter((val) => val.date || val.choice);
  $: value = filteredValueCopy.length > 0 ? filteredValueCopy : null;

  function addEntry() {
    valueCopy = [...valueCopy, {}];
  }

  function removeEntry(index) {
    valueCopy = valueCopy.filter((val, i) => i !== index);
  }

  const anySelectedAsCurrent = (values) => values.some((val) => val.current);
  const isCurrentRequired = (values) =>
    values.length > 0 && !anySelectedAsCurrent(values);
</script>

<div class="json_date_choice_field whitespace-nowrap">
  <table class="w-full">
    <thead>
      <tr>
        <th class="font-normal">{$_("Current")}</th>
        <th class="font-normal">{$_("Date")}</th>
        <th class="font-normal">{$_("Choice")}</th>
        <th />
      </tr>
    </thead>
    <tbody>
      {#each valueCopy as val, i}
        <tr class:is-current={val.current}>
          <td class="text-center p-1">
            <div class="form-check form-check-inline">
              <input
                required={isCurrentRequired(valueCopy)}
                type="checkbox"
                bind:checked={val.current}
                disabled={!val.date || !val.choice}
              />
            </div>
          </td>
          <td class="w-36 p-1">
            <LowLevelDateYearField
              bind:value={val.date}
              required={val.choice}
              name={formfield.name}
            />
          </td>
          <td class="w-2/3 p-1">
            <TypedChoiceField bind:value={val.choice} {formfield} required={val.date} />
          </td>

          <td class="p-1">
            <button type="button" on:click={addEntry}>
              <PlusIcon class="w-5 h-5 text-black" />
            </button>
            <button
              type="button"
              disabled={valueCopy.length <= 1}
              on:click={() => removeEntry(i)}
            >
              <MinusIcon class="w-5 h-5 text-red-600" />
            </button>
          </td>
        </tr>
      {/each}
    </tbody>
  </table>
</div>
