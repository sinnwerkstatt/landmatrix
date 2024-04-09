<script lang="ts">
  import type { InvestorHull } from "$lib/types/newtypes"

  import EditSubsection from "$components/EditSubsection.svelte"
  import EditField from "$components/Fields/EditField.svelte"

  export let investor: InvestorHull
  let version = investor.selected_version
  $: version = investor.selected_version
</script>

<form id="general">
  <EditSubsection id="investor.general_info">
    <EditField bind:value={version.name} fieldname="name" model="investor" showLabel />
    <EditField
      bind:value={version.country}
      extras={{ required: true }}
      fieldname="country"
      model="investor"
      showLabel
    />
    <EditField
      bind:value={version.classification}
      fieldname="classification"
      model="investor"
      showLabel
    />
    <EditField
      bind:value={version.homepage}
      fieldname="homepage"
      model="investor"
      showLabel
    />
    <EditField
      bind:value={version.opencorporates}
      fieldname="opencorporates"
      model="investor"
      showLabel
    />
    <EditField
      bind:value={version.comment}
      fieldname="comment"
      model="investor"
      showLabel
    />
  </EditSubsection>
</form>
