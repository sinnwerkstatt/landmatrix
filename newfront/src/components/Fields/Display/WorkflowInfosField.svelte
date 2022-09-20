<script lang="ts">
  import { slide } from "svelte/transition"

  import type { WorkflowInfo as WFInfo } from "$lib/types/generics"

  import type { FormField } from "$components/Fields/fields"
  import ManageHeaderLogbookList from "$components/Management/ManageHeaderLogbookList.svelte"
  import WorkflowInfo from "$components/Management/WorkflowInfo.svelte"

  export let value: WFInfo[]
  export let formfield: FormField

  let showMoreInfos = false

  function clickOutside(element, callbackFunction) {
    function onClick(event) {
      if (!element.contains(event.target)) {
        callbackFunction()
      }
    }

    document.body.addEventListener("click", onClick)
    return {
      update(newCallbackFunction) {
        callbackFunction = newCallbackFunction
      },
      destroy() {
        document.body.removeEventListener("click", onClick)
      },
    }
  }
</script>

<div
  class="workflowinfo-field"
  data-name={formfield?.name ?? ""}
  on:click={event => {
    showMoreInfos = !showMoreInfos
    event.stopPropagation()
  }}
>
  <WorkflowInfo info={value[0]} />
  {#if showMoreInfos}
    <div
      transition:slide
      use:clickOutside={() => {
        showMoreInfos = !showMoreInfos
      }}
      class="absolute top-0 z-10 mx-1 w-[368px] rounded-sm border border-black bg-lm-warmgray shadow-md"
    >
      <ManageHeaderLogbookList workflowinfos={value} />
    </div>
  {/if}
</div>
