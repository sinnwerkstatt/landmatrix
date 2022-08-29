<script lang="ts">
  import { _ } from "svelte-i18n";
  import { createValueCopy, syncValue } from "$components/Fields/JSONField";
  import MinusIcon from "$components/icons/MinusIcon.svelte";
  import PlusIcon from "$components/icons/PlusIcon.svelte";
  import type { FormField } from "../fields";
  import LowLevelDateYearField from "./LowLevelDateYearField.svelte";
  import LowLevelDecimalField from "./LowLevelDecimalField.svelte";
  import TypedChoicesField from "./TypedChoicesField.svelte";

  interface JSONExportsField {
    date?: string;
    area?: number;
    choices?: string;
    yield?: number;
    export?: number;
    current?: boolean;
  }

  export let formfield: FormField;
  export let value: Array<JSONExportsField> | null;

  let valueCopy = createValueCopy(value);
  $: value = syncValue(
    (val) => !!(val.date || val.area || val.choices || val.yield || val.export),
    valueCopy
  );

  function addEntry() {
    valueCopy = [...valueCopy, {}];
  }

  function removeEntry(index) {
    valueCopy = valueCopy.filter((val, i) => i !== index);
  }

  const anySelectedAsCurrent = (values) => values.some((val) => val.current);
  const isCurrentRequired = (values): boolean =>
    values.length > 0 && !anySelectedAsCurrent(values);
</script>

<div class="json_date_area_field whitespace-nowrap">
  <table class="w-full">
    <thead>
      <tr>
        <th class="font-normal">{$_("Current")}</th>
        <th class="font-normal">{$_("Date")}</th>
        <th class="font-normal">{$_("Area (ha)")}</th>
        <th class="font-normal">{$_("Choices")}</th>
        <th class="font-normal">{$_("Yield (tons)")}</th>
        <th class="font-normal">{$_("Export (%)")}</th>
        <th />
      </tr>
    </thead>
    <tbody>
      {#each valueCopy as val, i}
        <tr class:is-current={val.current}>
          <td class="p-1 text-center">
            <input
              type="checkbox"
              bind:checked={val.current}
              name="{formfield.name}_current"
              required={isCurrentRequired(valueCopy)}
              disabled={!val.date &&
                !val.area &&
                !val.choices &&
                !val.yield &&
                !val.export}
            />
          </td>

          <td class="w-1/5 p-1">
            <LowLevelDateYearField
              bind:value={val.date}
              required={formfield.required}
              name={formfield.name}
            />
          </td>
          <td class="w-1/5 p-1">
            <LowLevelDecimalField
              bind:value={val.area}
              required={formfield.required}
              name={formfield.name}
              unit="ha"
            />
          </td>
          <td class="w-1/5 p-1">
            <TypedChoicesField
              bind:value={val.choices}
              {formfield}
              required={formfield.required}
            />
          </td>
          <td class="w-1/5 p-1">
            <LowLevelDecimalField
              bind:value={val.yield}
              required={formfield.required}
              unit="tons"
              name={formfield.name}
            />
          </td>
          <td class="w-1/5 p-1">
            <LowLevelDecimalField
              bind:value={val.export}
              required={formfield.required}
              name={formfield.name}
              unit="%"
              max="100"
            />
          </td>

          <td class="p-1">
            <button type="button" on:click={addEntry}>
              <PlusIcon class="h-5 w-5 text-black" />
            </button>
            <button
              type="button"
              disabled={valueCopy.length <= 1}
              on:click={() => removeEntry(i)}
            >
              <MinusIcon class="h-5 w-5 text-red-600" />
            </button>
          </td>
        </tr>
      {/each}
    </tbody>
  </table>
</div>
