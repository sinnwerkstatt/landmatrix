<script lang="ts">
  import type { DealHull } from "$lib/types/data"

  import EditSubsection from "$components/Data/EditSubsection.svelte"
  import EditField from "$components/Fields/EditField.svelte"

  interface Props {
    deal: DealHull
  }

  let { deal = $bindable() }: Props = $props()
</script>

<form id="gender_related_info" class="pb-52">
  <EditSubsection id="gender_related_information">
    <EditField
      bind:value={deal.selected_version.gender_related_information}
      fieldname="gender_related_information"
      showLabel
    />
  </EditSubsection>
</form>
