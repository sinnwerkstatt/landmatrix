<script lang="ts">
  import { _ } from "svelte-i18n"

  import TypedChoiceField from "$components/Fields/Edit/TypedChoiceField.svelte"
  import { createValueCopy, syncValue } from "$components/Fields/JSONField"
  import MinusIcon from "$components/icons/MinusIcon.svelte"
  import PlusIcon from "$components/icons/PlusIcon.svelte"

  import type { FormField } from "../fields"

  interface JSONActorsField {
    name?: string
    role?: string
  }

  export let formfield: FormField
  export let value: Array<JSONActorsField> | null

  let valueCopy = createValueCopy(value)
  $: value = syncValue(val => !!(val.name || val.role), valueCopy)

  function addEntry() {
    valueCopy = [...valueCopy, {}]
  }
  function removeEntry(index) {
    valueCopy = valueCopy.filter((val, i) => i !== index)
  }
</script>

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
        <td class="w-1/3">
          <input
            type="text"
            bind:value={val.name}
            class="inpt"
            name="{formfield.name}_{i}_name"
          />
        </td>
        <td>
          <!-- Required by backend if name set -->
          <TypedChoiceField
            bind:value={val.role}
            formfield={{ ...formfield, name: `${formfield.name}_${i}_role` }}
            required={!!val.name}
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
