<script lang="ts">
  import type { WorkflowInfoType } from "$lib/types/data"

  import Modal from "$components/Modal.svelte"
  import WorkflowInfoNew from "$components/New/WorkflowInfoNew.svelte"

  export let value: WorkflowInfoType[]

  let showMoreInfos = false
</script>

<div>
  <button
    class="w-full cursor-pointer text-left"
    on:click={() => (showMoreInfos = true)}
    type="button"
  >
    <WorkflowInfoNew info={value[0]} isDeal />
  </button>
</div>

<Modal bind:open={showMoreInfos} dismissible style="--open-speed: 100ms;">
  <div class="max-h-[80vh] min-w-[400px] max-w-[60vw]">
    {#each value as info}
      <WorkflowInfoNew {info} isDeal />
    {/each}
  </div>
</Modal>
