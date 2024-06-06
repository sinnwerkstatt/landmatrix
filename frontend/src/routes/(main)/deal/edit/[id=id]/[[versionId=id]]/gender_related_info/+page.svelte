<script lang="ts">
  import EditSubsection from "$components/EditSubsection.svelte"
  import EditField from "$components/Fields/EditField.svelte"

  import { mutableDeal } from "../store"

  export let data

  let version = data.deal.selected_version

  $: $mutableDeal.selected_version = version
</script>

<form id="gender_related_info" class="pb-52">
  <EditSubsection id="gender_related_information">
    <EditField
      bind:value={version.gender_related_information}
      fieldname="gender_related_information"
      showLabel
    />
  </EditSubsection>
</form>
