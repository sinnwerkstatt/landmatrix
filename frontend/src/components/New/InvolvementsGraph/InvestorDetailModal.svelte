<script lang="ts">
  import { _ } from "svelte-i18n"

  import { fieldChoices } from "$lib/stores"
  import type { Investor } from "$lib/types/investor"

  import CountryField from "$components/Fields/Display2/CountryField.svelte"
  import TextField from "$components/Fields/Display2/TextField.svelte"
  import Overlay from "$components/Overlay.svelte"

  export let visible: boolean
  export let investor: Investor
</script>

<Overlay on:close title="{investor.name} ({investor.id})" {visible}>
  <div>
    <TextField
      choices={$fieldChoices.investor.classification}
      fieldname="investor.classification"
      label={$_("Classification")}
      value={investor.active_version__classification}
    />
    <CountryField
      fieldname="investor.country"
      label={$_("Country of registration/origin")}
      value={investor.active_version__country_id}
    />
    <TextField
      fieldname="investor.homepage"
      label={$_("Investor homepage")}
      value={investor.active_version__homepage}
    />
    <TextField
      fieldname="investor.comment"
      label={$_("Comment")}
      value={investor.active_version__comment}
    />
    <div class="w-100 mt-8">
      <a
        class="investor"
        href="/investor/{investor.id}"
        rel="noreferrer"
        target="_blank"
      >
        {$_("More details about this investor")}
      </a>
    </div>
  </div>
</Overlay>
