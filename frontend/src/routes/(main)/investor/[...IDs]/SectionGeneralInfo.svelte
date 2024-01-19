<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { InvestorVersion2 } from "$lib/types/newtypes"

  import DisplayField from "$components/Fields/DisplayField.svelte"

  export let version: InvestorVersion2
</script>

<section>
  <div class="mt-2 space-y-4">
    <h3 class="my-0">{$_("General info")}</h3>
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
  </div>
</section>
