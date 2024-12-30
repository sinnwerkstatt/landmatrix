<script lang="ts">
  import type { MouseEventHandler } from "svelte/elements"

  import PlusIcon from "$components/icons/PlusIcon.svelte"

  interface Props {
    onclick?: MouseEventHandler<HTMLButtonElement>
  }
  let { onclick }: Props = $props()
</script>

<button
  class="flex w-full items-center justify-center border border-gray-200 p-2"
  {onclick}
  type="button"
>
  <PlusIcon class="size-7" />
</button>
