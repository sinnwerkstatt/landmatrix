<script lang="ts">
  import type { WorkflowInfo } from "$lib/types/data"

  import Modal from "$components/Modal.svelte"
  import WorkflowInfoNew from "$components/New/WorkflowInfoNew.svelte"

  interface Props {
    value: WorkflowInfo[]
  }

  let { value }: Props = $props()

  let open = $state(false)
</script>

<div>
  <button
    class="w-full cursor-pointer text-left"
    onclick={() => (open = true)}
    type="button"
  >
    <WorkflowInfoNew info={value[0]} isDeal />
  </button>
</div>

<Modal bind:open dismissible style="--open-speed: 100ms;">
  <div class="max-h-[80vh] min-w-[400px] max-w-[60vw]">
    {#each value as info}
      <WorkflowInfoNew {info} isDeal />
    {/each}
  </div>
</Modal>
