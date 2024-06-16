<script lang="ts">
  import type { InvestorHull, InvestorVersion2 } from "$lib/types/data"

  import DisplayField from "$components/Fields/DisplayField.svelte"
  import Subsection from "$components/Subsection.svelte"

  export let investor: InvestorHull

  let version: InvestorVersion2 = investor.selected_version
  $: version = investor.selected_version
</script>

<Subsection id="investor.general_info" obj={version}>
  <DisplayField fieldname="name" model="investor" showLabel value={version.name} />
  <DisplayField
    fieldname="country_id"
    model="investor"
    showLabel
    value={version.country_id}
  />
  <DisplayField
    fieldname="classification"
    model="investor"
    showLabel
    value={version.classification}
  />
  <DisplayField
    fieldname="homepage"
    model="investor"
    showLabel
    value={version.homepage}
  />
  <DisplayField
    fieldname="opencorporates"
    model="investor"
    showLabel
    value={version.opencorporates}
  />
  <DisplayField
    fieldname="comment"
    model="investor"
    showLabel
    value={version.comment}
  />
</Subsection>
