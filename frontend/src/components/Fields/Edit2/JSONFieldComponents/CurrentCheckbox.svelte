<script lang="ts">
  import { _ } from "svelte-i18n"

  import { labelClass } from "$components/Fields/Edit2/JSONFieldComponents/consts"

  export let checked: boolean
  export let name: string

  export let required = false
  export let disabled = false
</script>

<label class={labelClass}>
  {$_("Current")}
  <input
    bind:checked
    class="h-5 w-5 accent-violet-400 ring-red-600"
    class:ring-2={required}
    {name}
    {required}
    {disabled}
    type="checkbox"
  />
</label>
