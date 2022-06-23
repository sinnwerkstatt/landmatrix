<script lang="ts">
  import { _ } from "svelte-i18n";
  import MinusIcon from "$components/icons/MinusIcon.svelte";
  import PlusIcon from "$components/icons/PlusIcon.svelte";
  import type { FormField } from "../fields";
  import LowLevelDateYearField from "./LowLevelDateYearField.svelte";
  import LowLevelDecimalField from "./LowLevelDecimalField.svelte";

  interface JSONDateAreaField {
    date?: string;
    area?: number;
    current?: boolean;
  }

  export let formfield: FormField;
  export let value: Array<JSONDateAreaField>;
  let current = value?.map((val) => val.current)?.indexOf(true) ?? -1;

  // create valueCopy to avoid overwriting null in db by [] or so
  let valueCopy: Array<JSONDateAreaField> = JSON.parse(JSON.stringify(value ?? [{}]));
  $: filteredValueCopy = valueCopy.filter((val) => val.date || val.area);
  $: value = filteredValueCopy.length > 0 ? filteredValueCopy : null;

  function updateCurrent(index) {
    valueCopy = valueCopy.map((val) => ({ ...val, current: undefined }));
    valueCopy[index].current = true;
    valueCopy = valueCopy;
  }
  function addEntry() {
    valueCopy = [...valueCopy, {}];
  }
  function removeEntry(index) {
    if (current === index) {
      current = -1;
    } else if (current > index) {
      current--;
    }
    valueCopy = valueCopy.filter((val, i) => i !== index);
  }
</script>

<div class="json_date_area_field whitespace-nowrap">
  <table class="w-full">
    <thead>
      <tr>
        <th>{$_("Current")}</th>
        <th>{$_("Date")}</th>
        <th>{$_("Area (ha)")}</th>
        <th />
      </tr>
    </thead>
    <tbody>
      {#each valueCopy as val, i}
        <tr class:is-current={val.current}>
          <td class="text-center p-1" on:click={() => updateCurrent(i)}>
            <input
              type="radio"
              bind:group={current}
              name="{formfield.name}_current"
              required={valueCopy.length > 0}
              disabled={!val.date && !val.area}
              value={i}
            />
          </td>

          <td class="w-1/3 p-1">
            <LowLevelDateYearField
              bind:value={val.date}
              required={formfield.required}
              name={formfield.name}
            />
          </td>

          <td class="w-1/3 p-1">
            <LowLevelDecimalField
              bind:value={val.area}
              required={formfield.required}
              name={formfield.name}
              unit="ha"
            />
          </td>

          <td class="p-1">
            <button type="button" on:click={addEntry} name="plus_icon">
              <PlusIcon class="w-5 h-5 text-black" />
            </button>
            <button
              type="button"
              disabled={valueCopy.length <= 1}
              on:click={() => removeEntry(i)}
              name="minus_icon"
            >
              <MinusIcon class="w-5 h-5 text-red-600" />
            </button>
          </td>
        </tr>
      {/each}
    </tbody>
  </table>
</div>
