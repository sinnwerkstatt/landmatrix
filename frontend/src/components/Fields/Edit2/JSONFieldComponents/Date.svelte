<script lang="ts">
  import { _ } from "svelte-i18n"

  import { labelClass } from "$components/Fields/Edit2/JSONFieldComponents/consts"
  import LowLevelDateYearField from "$components/Fields/Edit2/LowLevelDateYearField.svelte"

  export let value: string | null
  export let name: string
</script>

<label class={labelClass} for={undefined}>
  {$_("Date")}
  <LowLevelDateYearField bind:value {name} />
</label>
