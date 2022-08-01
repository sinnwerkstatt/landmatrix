<script lang="ts">
  import { _ } from "svelte-i18n";
  import { createValueCopy, syncValue } from "$components/Fields/JSONField";
  import MinusIcon from "$components/icons/MinusIcon.svelte";
  import PlusIcon from "$components/icons/PlusIcon.svelte";
  import type { FormField } from "../fields";

  interface JSONActorsField {
    name?: string;
    role?: string;
  }

  export let formfield: FormField;
  export let value: Array<JSONActorsField> | null;

  let valueCopy = createValueCopy(value);
  $: value = syncValue((val) => !!(val.name || val.role), valueCopy);

  function addEntry() {
    valueCopy = [...valueCopy, {}];
  }
  function removeEntry(index) {
    valueCopy = valueCopy.filter((val, i) => i !== index);
  }
</script>

<div class="json_date_area_field whitespace-nowrap">
  <table class="w-full">
    <thead>
      <tr>
        <th class="font-normal">{$_("Name")}</th>
        <th class="font-normal">{$_("Role")}</th>
      </tr>
    </thead>
    <tbody>
      {#each valueCopy as val, i}
        <tr>
          <td class="w-1/2">
            <input
              type="text"
              bind:value={val.name}
              class="inpt"
              name={formfield.name}
            />
          </td>
          <td>
            <select bind:value={val.role} class="inpt" name={formfield.name}>
              <option />
              {#each Object.entries(formfield.choices) as [value, label]}
                <option {value}>{label}</option>
              {/each}
            </select>
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
