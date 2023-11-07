<script lang="ts">
  import { _ } from "svelte-i18n"

  import AtIcon from "$components/icons/AtIcon.svelte"

  import type { FormField } from "../fields"

  export let formfield: FormField
  export let value: string
</script>

<input
  bind:value
  type="email"
  class="inpt"
  placeholder={$_(formfield.label)}
  maxlength={formfield.max_length}
  name={formfield.name}
/>
<div
  class="flex items-center justify-center border border-l-0 border-gray-300 bg-gray-200 px-3 py-1.5 text-gray-600"
>
  <AtIcon class="h-4 w-4" />
</div>
