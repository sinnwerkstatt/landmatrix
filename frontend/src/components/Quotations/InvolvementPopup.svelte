<script lang="ts">
  import type { Involvement } from "$lib/types/data"
  import type { SubmodelEntry } from "$lib/utils/dataProcessing"

  import InvestorCard from "$components/Data/Investor/Sections/Involvements/InvestorCard.svelte"

  interface Props {
    entry: SubmodelEntry
  }

  let { entry }: Props = $props()

  const involvement = $derived(entry as Involvement)
</script>

<InvestorCard isParent {involvement} />
