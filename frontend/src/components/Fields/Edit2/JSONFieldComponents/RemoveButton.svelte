<script lang="ts">
  import { _ } from "svelte-i18n"
  import type { MouseEventHandler } from "svelte/elements"

  import TrashIcon from "$components/icons/TrashIcon.svelte"

  interface Props {
    disabled?: boolean
    onclick?: MouseEventHandler<HTMLButtonElement>
  }

  let { disabled = false, onclick }: Props = $props()
</script>

<button {disabled} {onclick} title={$_("Remove entry")} type="button">
  <TrashIcon class="h-5 w-5 {!disabled ? 'text-red-600' : 'text-gray-200'}" />
</button>
