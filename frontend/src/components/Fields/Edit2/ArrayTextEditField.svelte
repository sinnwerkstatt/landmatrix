<script lang="ts">
  import { _ } from "svelte-i18n"

  import AddButton from "$components/Fields/Edit2/JSONFieldComponents/AddButton.svelte"
  import RemoveButton from "$components/Fields/Edit2/JSONFieldComponents/RemoveButton.svelte"

  import { cardClass } from "./JSONFieldComponents/consts"

  interface Props {
    value: string[]
    fieldname: string
  }

  let { value = $bindable(), fieldname }: Props = $props()

  let valueCopy: string[] = $state(value.length ? $state.snapshot(value) : [""])

  const updateVal = () => {
    value = valueCopy.filter(val => val != "")
  }

  const addEntry = () => {
    valueCopy = [...valueCopy, ""]
    updateVal()
  }

  const removeEntry = (index: number) => {
    valueCopy = valueCopy.filter((_val, i) => i !== index)
    updateVal()
  }
</script>

<div class="grid gap-2 lg:grid-cols-2 xl:grid-cols-3">
  {#each valueCopy as _val, i}
    <div class={cardClass}>
      <input
        class="inpt"
        type="text"
        bind:value={valueCopy[i]}
        name="{fieldname}_{i}"
        placeholder={$_("Name")}
        oninput={updateVal}
      />

      <RemoveButton disabled={valueCopy.length <= 1} onclick={() => removeEntry(i)} />
    </div>
  {/each}

  <AddButton onclick={addEntry} />
</div>
