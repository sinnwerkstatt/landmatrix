<script lang="ts">
  import type { InvestorVersion2 } from "$lib/types/newtypes"

  import DisplayField from "$components/Fields/DisplayField.svelte"
  import Subsection from "$components/Subsection.svelte"

  export let version: InvestorVersion2
</script>

<Subsection id="investor.general_info" obj={version}>
  <DisplayField fieldname="name" model="investor" showLabel value={version.name} />
  <DisplayField
    fieldname="country"
    model="investor"
    showLabel
    value={version.country}
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
