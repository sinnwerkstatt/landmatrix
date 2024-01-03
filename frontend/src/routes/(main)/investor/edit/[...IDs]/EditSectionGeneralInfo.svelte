<script lang="ts">
  import { _ } from "svelte-i18n"

  import { fieldChoices } from "$lib/stores"
  import type { InvestorHull } from "$lib/types/newtypes"

  import EditSubsection from "$components/EditSubsection.svelte"
  import ChoicesField from "$components/Fields/Edit2/ChoicesField.svelte"
  import CountryField from "$components/Fields/Edit2/CountryField.svelte"
  import TextField from "$components/Fields/Edit2/TextField.svelte"

  export let investor: InvestorHull
  let version = investor.selected_version
  $: version = investor.selected_version
</script>

<form id="general">
  <EditSubsection title={$_("General info")}>
    <TextField bind:value={version.name} fieldname="investor.name" label={$_("Name")} />
    <CountryField
      bind:value={version.country}
      fieldname="investor.country"
      label={$_("Country of registration/origin")}
      required
    />
    <ChoicesField
      bind:value={version.classification}
      choices={$fieldChoices.investor.classification}
      fieldname="investor.classification"
      label={$_("Classification")}
    />

    <TextField
      bind:value={version.homepage}
      fieldname="investor.homepage"
      label={$_("Investor homepage")}
      isURL
    />
    <TextField
      bind:value={version.opencorporates}
      fieldname="investor.opencorporates"
      label={$_("Opencorporates link")}
      isURL
    />

    <TextField
      bind:value={version.comment}
      fieldname="investor.comment"
      label={$_("Comment")}
      multiline
    />
  </EditSubsection>
</form>
