<script lang="ts">
  import type { InvestorHull } from "$lib/types/data"

  import EditBase from "./Edit.svelte"

  interface Props {
    investor: InvestorHull
  }

  let { investor = $bindable() }: Props = $props()
</script>

<EditBase bind:investor />
