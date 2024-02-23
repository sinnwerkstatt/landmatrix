<script lang="ts">
  import { _ } from "svelte-i18n"

  import AddButton from "$components/Fields/Edit2/JSONFieldComponents/AddButton.svelte"
  import RemoveButton from "$components/Fields/Edit2/JSONFieldComponents/RemoveButton.svelte"

  import { cardClass } from "./JSONFieldComponents/consts"

  export let value: string[]
  export let fieldname: string

  let valueCopy = structuredClone<string[]>(value.length ? value : [""])

  $: value = valueCopy.filter(val => val != "")

  const addEntry = () => (valueCopy = [...valueCopy, ""])

  const removeEntry = (index: number) => {
    valueCopy = valueCopy.filter((_val, i) => i !== index)
  }
</script>

<div class="grid gap-2 lg:grid-cols-2 xl:grid-cols-3">
  {#each valueCopy as val, i}
    <div class={cardClass}>
      <input
        class="inpt"
        type="text"
        bind:value={val}
        name="{fieldname}_{i}"
        placeholder={$_("Name")}
      />

      <RemoveButton disabled={valueCopy.length <= 1} on:click={() => removeEntry(i)} />
    </div>
  {/each}

  <AddButton on:click={addEntry} />
</div>
