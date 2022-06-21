<script lang="ts">
  import WorkflowInfo from "./WorkflowInfo.svelte";

  export let workflowinfos = [];
</script>

<div
  class="-mr-3 shadow-inner bg-neutral-400 overflow-y-scroll cursor-default h-full px-[2px] py-1 max-h-[330px]"
>
  {#each workflowinfos as info}
    <div>
      <WorkflowInfo {info} />
    </div>
  {/each}
</div>
