<script lang="ts">
  import { _ } from "svelte-i18n";
  import MinusIcon from "$components/icons/MinusIcon.svelte";
  import PlusIcon from "$components/icons/PlusIcon.svelte";
  import type { FormField } from "../fields";
  import LowLevelDateYearField from "./LowLevelDateYearField.svelte";
  import LowLevelDecimalField from "./LowLevelDecimalField.svelte";
  import TextField from "./TextField.svelte";

  interface JSONActorsField {
    name?: string;
    role?: string;
  }

  export let formfield: FormField;
  export let value: Array<JSONActorsField>;

  // create valueCopy to avoid overwriting null in db by [] or so
  let valueCopy: Array<JSONActorsField> = JSON.parse(JSON.stringify(value ?? [{}]));
  $: filteredValueCopy = valueCopy.filter((val) => val.name || val.role);
  $: value = filteredValueCopy.length > 0 ? filteredValueCopy : null;

  function addEntry() {
    valueCopy = [...valueCopy, {}];
  }
  function removeEntry(index) {
    valueCopy = valueCopy.filter((val, i) => i !== index);
  }
</script>

<div class="json_date_area_field whitespace-nowrap">
  <!--{JSON.stringify(value)}-->
  <!--{JSON.stringify(Object.entries(formfield.choices))}-->
  <table class="w-full">
    <thead>
      <tr>
        <th>{$_("Name")}</th>
        <th>{$_("Role")}</th>
      </tr>
    </thead>
    <tbody>
      {#each valueCopy as val, i}
        <tr>
          <td class="w-1/2">
            <input type="text" bind:value={val.name} class="inpt" />
          </td>
          <div class="typed_choice_field">
            <select bind:value={val.role} class="inpt" name={formfield.name}>
              <option />
              {#each Object.entries(formfield.choices) as [value, label]}
                <option {value}>{label}</option>
              {/each}
            </select>
          </div>

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
