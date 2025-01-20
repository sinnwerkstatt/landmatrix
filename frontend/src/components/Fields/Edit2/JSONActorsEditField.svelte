<script lang="ts">
  import { _ } from "svelte-i18n"
  import Select from "svelte-select"

  import { dealChoices } from "$lib/fieldChoices"
  import type { InvolvedActor } from "$lib/types/data"

  import AddButton from "$components/Fields/Edit2/JSONFieldComponents/AddButton.svelte"
  import {
    cardClass,
    labelClass,
  } from "$components/Fields/Edit2/JSONFieldComponents/consts"
  import RemoveButton from "$components/Fields/Edit2/JSONFieldComponents/RemoveButton.svelte"

  interface Props {
    value: InvolvedActor[]
    fieldname?: string
  }

  let { value = $bindable(), fieldname = "involved_actors" }: Props = $props()

  const emptyEntry: InvolvedActor = {
    name: "",
    role: null,
  }
  let valueCopy: InvolvedActor[] = $state(
    value.length ? $state.snapshot(value) : [structuredClone(emptyEntry)],
  )

  const updateVal = () => {
    value = valueCopy.filter(val => !!(val.name || val.role))
  }

  const addEntry = () => {
    valueCopy = [...valueCopy, structuredClone(emptyEntry)]
    updateVal()
  }

  const removeEntry = (index: number) => {
    valueCopy = valueCopy.filter((_val, i) => i !== index)
    updateVal()
  }
</script>

<div class="grid gap-2 lg:grid-cols-2 xl:grid-cols-3">
  {#each valueCopy as val, i}
    <div class={cardClass}>
      <label class={labelClass} for={undefined}>
        {$_("Name")}
        <input
          bind:value={val.name}
          type="text"
          class="inpt"
          placeholder={$_("Name")}
          name="{fieldname}_{i}_name"
          oninput={updateVal}
        />
      </label>

      <label class={labelClass} for={undefined}>
        {$_("Role")}
        <Select
          value={$dealChoices.actors.find(i => i.value === val.role)}
          on:change={e => {
            val.role = e.detail.value
            updateVal()
          }}
          on:clear={() => {
            val.role = null
            updateVal()
          }}
          required={!!val.name}
          items={$dealChoices.actors}
          showChevron
          hasError={!!val.name && !value}
          class={!!val.name && !val.role ? "!border-red-600" : ""}
        />
      </label>

      <RemoveButton disabled={valueCopy.length <= 1} onclick={() => removeEntry(i)} />
    </div>
  {/each}
  <AddButton onclick={addEntry} />
</div>
