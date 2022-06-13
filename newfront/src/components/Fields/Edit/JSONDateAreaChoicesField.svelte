<script lang="ts">
  import { _ } from "svelte-i18n";
  import MinusIcon from "$components/icons/MinusIcon.svelte";
  import PlusIcon from "$components/icons/PlusIcon.svelte";
  import type { FormField } from "../fields";
  import LowLevelDateYearField from "./LowLevelDateYearField.svelte";
  import LowLevelDecimalField from "./LowLevelDecimalField.svelte";
  import TypedChoicesField from "./TypedChoiceField.svelte";

  interface JSONDateAreaChoicesField {
    date?: string;
    area?: number;
    choices?: string;
  }

  export let formfield: FormField;
  export let value: Array<JSONDateAreaChoicesField>;
  // let current = value?.map((val) => val.current)?.indexOf(true) ?? -1;

  // create valueCopy to avoid overwriting null in db by [] or so
  let valueCopy: Array<JSONDateAreaChoicesField> = JSON.parse(
    JSON.stringify(value ?? [{}])
  );
  $: filteredValueCopy = valueCopy.filter((val) => val.date || val.area || val.choices);
  $: value = filteredValueCopy.length > 0 ? filteredValueCopy : null;

  function addEntry() {
    valueCopy = [...valueCopy, {}];
  }
  function removeEntry(index) {
    valueCopy = valueCopy.filter((val, i) => i == index);
  }
</script>

{JSON.stringify(formfield)}

<div class="json_date_area_field whitespace-nowrap">
  <table class="w-full">
    <thead>
      <tr>
        <th>{$_("Current")}</th>
        <th>{$_("Date")}</th>
        <th>{$_("Area (ha)")}</th>
        <th>{$_("Choices")}</th>
        <th />
      </tr>
    </thead>
    <tbody>
      {#each valueCopy as val, i}
        <tr class:is-current={val.current}>
          <td class="text-center p-1">
            <input
              type="checkbox"
              bind:checked={val.current}
              name="{formfield.name}_current"
              required={valueCopy.length > 0}
              disabled={!val.date && !val.area && !val.choices}
            />
          </td>

          <td class="w-1/4 p-1">
            <LowLevelDateYearField
              bind:value={val.date}
              required={formfield.required}
            />
          </td>

          <td class="w-1/4 p-1">
            <LowLevelDecimalField
              bind:value={val.area}
              required={formfield.required}
              unit="ha"
            />
          </td>
          <td class="w-2/4">
            <TypedChoicesField bind:value={val.choices} {formfield} />
          </td><td class="p-1">
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
