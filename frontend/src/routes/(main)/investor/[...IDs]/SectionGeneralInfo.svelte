<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { InvestorVersion2 } from "$lib/types/newtypes"

  import CountryField from "$components/Fields/Display2/CountryField.svelte"
  import TextField from "$components/Fields/Display2/TextField.svelte"

  export let version: InvestorVersion2
</script>

<section>
  <div class="mt-2 space-y-4">
    <h3 class="my-0">{$_("General info")}</h3>
    <TextField fieldname="investor.name" label={$_("Name")} value={version.name} />
    <CountryField
      fieldname="investor.country"
      label={$_("Country of registration/origin")}
      value={version.country}
    />
    <TextField
      fieldname="investor.classification"
      label={$_("Classification")}
      value={version.classification}
    />
    <TextField
      fieldname="investor.homepage"
      label={$_("Investor homepage")}
      value={version.homepage}
    />
    <TextField
      fieldname="investor.opencorporates"
      label={$_("Opencorporates link")}
      value={version.opencorporates}
    />
    <TextField
      fieldname="investor.comment"
      label={$_("Comment")}
      value={version.comment}
    />
  </div>
</section>
