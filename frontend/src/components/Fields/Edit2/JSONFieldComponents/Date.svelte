<script lang="ts">
  import { _ } from "svelte-i18n"

  import { labelClass } from "$components/Fields/Edit2/JSONFieldComponents/consts"
  import LowLevelDateYearField from "$components/Fields/Edit2/LowLevelDateYearField.svelte"

  export let value: string | null = null
  export let name: string

  export let label = $_("Date")
</script>

<label class={labelClass} for={undefined}>
  {label}
  <LowLevelDateYearField bind:value {name} />
</label>
