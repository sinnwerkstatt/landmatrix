<script lang="ts">
  import { _ } from "svelte-i18n"

  import { labelClass } from "$components/Fields/Edit2/JSONFieldComponents/consts"

  export let value: number
  export let name: string

  export let required = false
  export let disabled = false

  export let group: number
</script>

<label class={labelClass}>
  {$_("Current")}
  <input
    {value}
    class="h-5 w-5 accent-violet-400 ring-red-600"
    class:ring-2={required}
    {name}
    {required}
    {disabled}
    type="radio"
    bind:group
    on:change
  />
</label>
