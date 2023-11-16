<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { DealVersion2 } from "$lib/types/newtypes"

  import DecimalField from "$components/Fields/Display2/DecimalField.svelte"
  import JSONDateAreaChoicesField from "$components/Fields/Display2/JSONDateAreaChoicesField.svelte"
  import TextField from "$components/Fields/Display2/TextField.svelte"

  export let version: DealVersion2
</script>

<section>
  <div class="mt-2 space-y-4">
    <h3 class="my-0">{$_("Land area")}</h3>

    <DecimalField
      fieldname="intended_size"
      unit={$_("ha")}
      value={version.intended_size}
      label={$_("Intended size (in ha)")}
    />
    <!--    contract_size  -->
    <!--     production_size -->
    <TextField
      fieldname="land_area_comment"
      value={version.land_area_comment}
      label={$_("Comment on land area")}
    />
  </div>

  <div class="mt-2 space-y-4">
    <h3 class="my-0">{$_("Intention of investment")}</h3>

    <JSONDateAreaChoicesField
      fieldname="intention_of_investment"
      value={version.intention_of_investment}
      label={$_("Intention of investment")}
    />
    <TextField
      fieldname="intention_of_investment_comment"
      value={version.intention_of_investment_comment}
      label={$_("Comment on intention of investment")}
    />
  </div>
</section>
