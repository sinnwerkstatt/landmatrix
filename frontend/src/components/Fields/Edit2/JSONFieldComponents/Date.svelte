<script lang="ts">
  import { _ } from "svelte-i18n"

  import { labelClass } from "$components/Fields/Edit2/JSONFieldComponents/consts"
  import LowLevelDateYearField from "$components/Fields/Edit2/LowLevelDateYearField.svelte"

  interface Props {
    value: string | null
    name: string
    label?: string
    onchange?: () => void
  }

  let { value = $bindable(), name, label = $_("Date"), onchange }: Props = $props()
</script>

<label class={labelClass} for={undefined}>
  {label}
  <LowLevelDateYearField bind:value {name} {onchange} />
</label>
