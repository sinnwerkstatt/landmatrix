<script lang="ts">
  import type { InvestorHull } from "$lib/types/data"

  import EditSubsection from "$components/Data/EditSubsection.svelte"
  import EditField from "$components/Fields/EditField.svelte"

  interface Props {
    investor: InvestorHull
  }

  let { investor = $bindable() }: Props = $props()
</script>

<form id="general">
  <EditSubsection id="investor.general_info">
    <EditField
      bind:value={investor.selected_version.name}
      fieldname="name"
      model="investor"
      showLabel
    />
    <EditField
      bind:value={investor.selected_version.country}
      extras={{ required: true }}
      fieldname="country_id"
      model="investor"
      showLabel
    />
    <EditField
      bind:value={investor.selected_version.classification}
      fieldname="classification"
      model="investor"
      showLabel
    />
    <EditField
      bind:value={investor.selected_version.homepage}
      fieldname="homepage"
      model="investor"
      showLabel
    />
    <EditField
      bind:value={investor.selected_version.opencorporates}
      fieldname="opencorporates"
      model="investor"
      showLabel
    />
    <EditField
      bind:value={investor.selected_version.comment}
      fieldname="comment"
      model="investor"
      showLabel
    />
  </EditSubsection>
</form>
