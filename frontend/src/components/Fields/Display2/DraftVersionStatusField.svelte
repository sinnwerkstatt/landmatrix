<script lang="ts">
  import { stateMap } from "$lib/newUtils"
  import type { Version2Status } from "$lib/types/newtypes"

  export let value: Version2Status
</script>

{$stateMap[value].title}
