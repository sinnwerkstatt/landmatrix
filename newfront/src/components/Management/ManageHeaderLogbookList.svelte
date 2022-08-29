<script lang="ts">
  import type { WorkflowInfo as WFInfo } from "$lib/types/generics"

  import WorkflowInfo from "./WorkflowInfo.svelte"

  export let workflowinfos: WFInfo[] = []
</script>

<div
  class="h-auto max-h-[330px] cursor-default overflow-y-scroll bg-lm-warmgray px-[2px] pt-1 pb-12 shadow-inner"
>
  {#each workflowinfos as info}
    <div>
      <WorkflowInfo {info} />
    </div>
  {/each}
</div>
