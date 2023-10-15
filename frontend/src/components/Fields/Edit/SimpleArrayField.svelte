<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { FormField } from "../fields"

  export let formfield: FormField
  export let value: Array<string | number> | null = []

  const onSelect = async x => {
    const opts = Array.from(x.target.options)
      .filter(o => o.selected)
      .map(o => o.value)
    value = opts.length === 0 ? null : opts
  }

  $: choices = formfield.choices?.filter(c => !!c.value)
</script>

{#if choices}
  <select
    value={value ?? []}
    on:change={onSelect}
    multiple
    class="inpt"
    name={formfield.name}
  >
    {#each choices as choice}
      <!-- The literal translation strings are defined in apps/landmatrix/models/choices.py -->
      <option value={choice.value}>{$_(choice.label)}</option>
    {/each}
  </select>
{:else}
  <div class="flex flex-col">
    <textarea
      value={value ? value.join("\n") : ""}
      on:input={x => (value = x.target.value ? x.target.value.split("\n") : null)}
      class="inpt"
      rows="5"
      name={formfield.name}
    />
    <small class="text-gray-500">
      {$_("Put each value on a new line, i.e. press enter between each name")}
    </small>
  </div>
{/if}
