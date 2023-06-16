<script lang="ts">
  import { _ } from "svelte-i18n"

  import LinkIcon from "$components/icons/LinkIcon.svelte"

  import type { FormField } from "../fields"

  export let formfield: FormField
  export let value: string
</script>

<div class="flex">
  <input
    bind:value
    type="url"
    class="inpt"
    placeholder={$_(formfield.label)}
    name={formfield.name}
    maxlength={formfield.max_length}
  />
  <div
    class="flex items-center justify-center border border-l-0 border-gray-300 bg-gray-200 py-1.5 px-3 text-gray-600"
  >
    <LinkIcon class="h-4 w-4" />
  </div>
</div>
