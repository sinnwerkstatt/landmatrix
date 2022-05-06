<script lang="ts">
  import { _ } from "svelte-i18n";
  import type { Deal, Location } from "$lib/types/deal";
  import DisplayField from "$components/Fields/DisplayField.svelte";

  export let deal: Deal;
  export let location: Location;
</script>

<h3>{$_("Deal")} #{deal.id}</h3>
<div class="deal-summary">
  <DisplayField
    wrapperClasses="mb-4"
    labelClasses="font-bold"
    valueClasses=""
    fieldname="level_of_accuracy"
    model="location"
    value={location.level_of_accuracy}
  />
  <DisplayField
    wrapperClasses="mb-4"
    labelClasses="font-bold"
    valueClasses=""
    fieldname="current_intention_of_investment"
    value={deal.current_intention_of_investment}
  />
  <DisplayField
    wrapperClasses="mb-4"
    labelClasses="font-bold"
    valueClasses=""
    fieldname="deal_size"
    value={deal.deal_size}
  />
  <DisplayField
    wrapperClasses="mb-4"
    labelClasses="font-bold"
    valueClasses=""
    fieldname="operating_company"
    value={deal.operating_company}
  />
</div>
<a href="/deal/{deal.id}/" class="btn btn-primary !text-white">
  {$_("More details")}
</a>
