<script lang="ts">
  import WorkflowInfo from "./WorkflowInfo.svelte";

  export let workflowinfos = [];
</script>

<div
  class="shadow-inner bg-lm-warmgray overflow-y-scroll cursor-default h-auto px-[2px] pt-1 pb-12 max-h-[330px]"
>
  {#each workflowinfos as info}
    <div>
      <WorkflowInfo {info} />
    </div>
  {/each}
</div>
