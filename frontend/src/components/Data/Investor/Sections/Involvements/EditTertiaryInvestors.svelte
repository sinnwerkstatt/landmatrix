<script lang="ts">
  import type { MutableInvestorHull } from "$lib/types/data"

  import EditBase from "./Edit.svelte"

  interface Props {
    investor: MutableInvestorHull
  }

  let { investor = $bindable() }: Props = $props()
</script>

<EditBase bind:investor tertiary />
