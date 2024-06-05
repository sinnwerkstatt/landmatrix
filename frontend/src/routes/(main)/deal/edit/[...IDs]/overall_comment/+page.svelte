<script lang="ts">
  import EditSubsection from "$components/EditSubsection.svelte"
  import EditField from "$components/Fields/EditField.svelte"

  import { mutableDeal } from "../store"

  export let data

  let version = data.deal.selected_version

  $: $mutableDeal.selected_version = version
</script>

<form id="overall_comment" class="pb-52">
  <EditSubsection id="overall_comment">
    <EditField
      bind:value={version.overall_comment}
      fieldname="overall_comment"
      showLabel
    />
  </EditSubsection>
</form>
