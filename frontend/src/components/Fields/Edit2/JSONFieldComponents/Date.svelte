<script lang="ts">
  import { _ } from "svelte-i18n"

  import LowLevelDateYearField from "$components/Fields/Edit/LowLevelDateYearField.svelte"
  import { labelClass } from "$components/Fields/Edit2/JSONFieldComponents/consts"

  export let value: string | null
  export let name: string
</script>

<label class={labelClass} for={undefined}>
  {$_("Date")}
  <LowLevelDateYearField bind:value {name} class="w-36" />
</label>
