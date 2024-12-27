<script lang="ts">
  import { stateMap } from "$lib/newUtils"
  import type { Version2Status } from "$lib/types/data"

  interface Props {
    value: Version2Status
  }

  let { value }: Props = $props()
</script>

{$stateMap[value].title}
