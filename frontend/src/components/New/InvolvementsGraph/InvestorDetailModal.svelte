<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { Investor } from "$lib/types/investor"

  import DisplayField from "$components/Fields/DisplayField.svelte"
  import Overlay from "$components/Overlay.svelte"

  export let visible: boolean
  export let investor: Investor
</script>

<Overlay on:close title="{investor.name} ({investor.id})" {visible}>
  <div>
    <DisplayField
      fieldname="classification"
      model="investor"
      showLabel
      value={investor.active_version__classification}
    />
    <DisplayField
      fieldname="country"
      model="investor"
      showLabel
      value={investor.active_version__country_id}
    />
    <DisplayField
      fieldname="homepage"
      model="investor"
      showLabel
      value={investor.active_version__homepage}
    />
    <DisplayField
      fieldname="comment"
      model="investor"
      showLabel
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
