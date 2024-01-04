<script lang="ts">
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import type { InvestorHull } from "$lib/types/newtypes.js"

  import SectionInvolvementsDealCard from "./SectionInvolvementsDealCard.svelte"
  import SectionInvolvementsInvestorCard from "./SectionInvolvementsInvestorCard.svelte"

  export let investor: InvestorHull

  $: filteredInvolvements = $page.data.user
    ? investor.involvements
    : investor.involvements.filter(i => !i.other_investor.deleted)
</script>

<section>
  <div class="mb-16 mt-2 space-y-4">
    <h3 class="heading3 my-0">{$_("Involvements")} ({filteredInvolvements.length})</h3>
    <div class="grid gap-4 lg:grid-cols-2 xl:grid-cols-3">
      {#each filteredInvolvements as involvement}
        <SectionInvolvementsInvestorCard {involvement} />
      {/each}
    </div>
  </div>
</section>

{#if investor.deals.length > 0}
  <section>
    <div class="mb-10 mt-2 space-y-4">
      <h3 class="heading3 my-0">
        {$_("Deals (Involvements as Operating company)")} ({investor.deals.length})
      </h3>
      <div class="grid gap-4 lg:grid-cols-2 xl:grid-cols-3">
        {#each investor.deals as deal}
          <SectionInvolvementsDealCard {deal} />
        {/each}
      </div>
    </div>
  </section>
{/if}
