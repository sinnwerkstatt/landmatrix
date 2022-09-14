<script lang="ts">
  import { slide } from "svelte/transition"

  import type { WorkflowInfo as WFInfo } from "$lib/types/generics"

  import type { FormField } from "$components/Fields/fields"
  import ManageHeaderLogbookList from "$components/Management/ManageHeaderLogbookList.svelte"
  import WorkflowInfo from "$components/Management/WorkflowInfo.svelte"

  export let value: object
  export let formfield: FormField
  export let model: "deal" | "investor" = "deal"
  export let objectId: number | null

  let showMoreInfos = false
  let moreInfos: WFInfo[] = []
</script>

<div
  class="workflowinfo-field"
  on:click={() => {
    showMoreInfos = !showMoreInfos
  }}
>
  <WorkflowInfo info={value[0]} />
  {#if showMoreInfos}
    <div
      transition:slide
      class="absolute z-10 mx-1 w-[22rem] rounded-sm bg-lm-warmgray shadow-md"
    >
      <h4 class="px-2">Logbooklist</h4>
      <ManageHeaderLogbookList workflowinfos={value} />
    </div>
  {/if}
</div>
