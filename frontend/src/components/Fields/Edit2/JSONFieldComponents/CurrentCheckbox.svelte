<script lang="ts">
  import { _ } from "svelte-i18n"

  import { labelClass } from "$components/Fields/Edit2/JSONFieldComponents/consts"

  interface Props {
    checked: boolean
    name: string
    required?: boolean
    disabled?: boolean
    onchange?: () => void
  }

  let {
    checked = $bindable(),
    name,
    required = false,
    disabled = false,
    onchange,
  }: Props = $props()
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
    {onchange}
    type="checkbox"
  />
</label>
