<script lang="ts">
  import { _ } from "svelte-i18n"
  import Select from "svelte-select"

  import { fieldChoices } from "$lib/stores"
  import type { InvolvedActor } from "$lib/types/newtypes"

  import AddButton from "$components/Fields/Edit2/JSONFieldComponents/AddButton.svelte"
  import {
    cardClass,
    labelClass,
  } from "$components/Fields/Edit2/JSONFieldComponents/consts"
  import RemoveButton from "$components/Fields/Edit2/JSONFieldComponents/RemoveButton.svelte"

  export let value: InvolvedActor[]
  export let fieldname = "involved_actors"

  const createEmptyEntry = (): InvolvedActor => ({ name: "", role: null })

  let valueCopy = structuredClone<InvolvedActor[]>(
    value.length ? value : [createEmptyEntry()],
  )

  $: value = valueCopy.filter(val => !!(val.name || val.role))

  const addEntry = () => (valueCopy = [...valueCopy, createEmptyEntry()])

  const removeEntry = (index: number) =>
    (valueCopy = valueCopy.filter((_val, i) => i !== index))
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
        />
      </label>

      <label class={labelClass} for={undefined}>
        {$_("Role")}
        <Select
          value={$fieldChoices.deal.actors.find(i => i.value === val.role)}
          on:change={e => (val.role = e.detail.value)}
          required={!!val.name}
          items={$fieldChoices.deal.actors}
          showChevron
          hasError={!!val.name && !value}
        />
        <!-- TODO Kurt is the role required? -->
      </label>

      <RemoveButton disabled={valueCopy.length <= 1} on:click={() => removeEntry(i)} />
    </div>
  {/each}
  <AddButton on:click={addEntry} />
</div>
