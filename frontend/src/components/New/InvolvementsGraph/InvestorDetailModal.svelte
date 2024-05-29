<script lang="ts">
  import { _ } from "svelte-i18n"

  import { Classification } from "$lib/types/investor"

  import DisplayField from "$components/Fields/DisplayField.svelte"
  import Overlay from "$components/Overlay.svelte"

  export let visible: boolean
  export let investor: {
    id: number
    name: string
    active_version__classification: Classification
    active_version__country_id: number | null
    active_version__homepage: string
    active_version__comment: string
  }
</script>

<Overlay
  on:close
  title="{investor.name} ({investor.id})"
  {visible}
  closeButtonText={$_("Close")}
  gotoLink={{
    href: `/investor/${investor.id}/`,
    title: $_("More details about this investor"),
    className: "btn-secondary",
  }}
>
  <DisplayField
    fieldname="classification"
    model="investor"
    showLabel
    value={investor.active_version__classification}
  />
  <DisplayField
    fieldname="country_id"
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
</Overlay>
