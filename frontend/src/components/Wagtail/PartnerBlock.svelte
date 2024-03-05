<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { Partner } from "$lib/types/wagtail"

  import PartnerSlider from "$components/PartnerSlider.svelte"

  export let value: Partner[]

  const partners = value.filter(p => p.role === "PARTNER")
  const donors = value.filter(p => p.role === "DONOR")
</script>

<div class="mx-auto bg-white py-6 text-center">
  {#if donors.length}
    <h2 class="heading3 text-gray-900">{$_("Donors")}</h2>
    <PartnerSlider partners={donors} perPage={3} />
  {/if}
  {#if partners.length}
    <h2 class="heading3 text-gray-900">{$_("Partners")}</h2>
    <PartnerSlider {partners} perPage={4} />
  {/if}
</div>
