<script lang="ts">
  import type { DealHull } from "$lib/types/data"

  import EditSubsection from "$components/Data/EditSubsection.svelte"
  import EditField from "$components/Fields/EditField.svelte"

  interface Props {
    deal: DealHull
  }

  let { deal = $bindable() }: Props = $props()
</script>

<form id="overall_comment" class="pb-52">
  <EditSubsection id="overall_comment">
    <EditField
      bind:value={deal.selected_version.overall_comment}
      fieldname="overall_comment"
      showLabel
    />
  </EditSubsection>
</form>
