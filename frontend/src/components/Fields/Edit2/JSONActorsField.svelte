<script lang="ts">
  import { _ } from "svelte-i18n"
  import Select from "svelte-select"

  import { fieldChoices } from "$lib/stores"
  import type { InvolvedActor } from "$lib/types/newtypes"

  import { LABEL_CLASS, VALUE_CLASS, WRAPPER_CLASS } from "$components/Fields/consts"
  import Label2 from "$components/Fields/Display2/Label2.svelte"
  import { createValueCopyNoNull } from "$components/Fields/Edit2/helpers"
  import MinusIcon from "$components/icons/MinusIcon.svelte"
  import PlusIcon from "$components/icons/PlusIcon.svelte"

  export let value: InvolvedActor[]
  export let fieldname: string = "involved_actors"
  export let label = ""
  export let wrapperClass = WRAPPER_CLASS
  export let labelClass = LABEL_CLASS
  export let valueClass = VALUE_CLASS

  let valueCopy = createValueCopyNoNull(value)
  $: value = valueCopy.filter(val => !!(val.name || val.role))

  function addEntry() {
    valueCopy = [...valueCopy, {}]
  }
  function removeEntry(index: number) {
    valueCopy = valueCopy.filter((val, i) => i !== index)
  }
</script>

<div class={wrapperClass} data-fieldname={fieldname}>
  {#if label}
    <Label2 value={label} class={labelClass} />
  {/if}
  <div class={valueClass}>
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
                name="{fieldname}_{i}_name"
              />
            </td>
            <td class="w-full">
              <Select
                value={$fieldChoices.deal.actors.find(i => i.value === val.role)}
                bind:justValue={val.role}
                required={!!val.name}
                items={$fieldChoices.deal.actors}
                showChevron
                hasError={!!val.name && !value}
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
</div>
