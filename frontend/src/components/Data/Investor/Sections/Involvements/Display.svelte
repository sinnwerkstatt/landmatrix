<script lang="ts">
  import { _ } from "svelte-i18n"

  import { type InvestorHull } from "$lib/types/data"

  import DealCard from "./DealCard.svelte"
  import InvestorCard from "./InvestorCard.svelte"

  interface Props {
    investor: InvestorHull
  }

  let { investor }: Props = $props()

  let parents = $derived(investor.selected_version.involvements)
</script>

<section>
  <div class="mb-16 mt-2 space-y-4">
    <h3 class="heading4 my-0">
      {parents.length}
      {$_("Parents (Involvements as child)")}
    </h3>
    <div class="grid gap-4 lg:grid-cols-2 xl:grid-cols-3">
      {#each parents as involvement (involvement.nid)}
        <InvestorCard isParent {involvement} />
      {/each}
    </div>
  </div>

  <div class="mb-16 mt-2 space-y-4">
    <h3 class="heading4 my-0">
      {investor.children.length}
      {$_("Children (Involvements as parent)")}
    </h3>
    <div class="grid gap-4 lg:grid-cols-2 xl:grid-cols-3">
      {#each investor.children as involvement (involvement.nid)}
        <InvestorCard {involvement} />
      {/each}
    </div>
  </div>

  {#if investor.deals.length > 0}
    <div class="mb-10 mt-2 space-y-4">
      <h3 class="heading4 my-0">
        {investor.deals.length}
        {$_("Deals (Involvements as Operating company)")}
      </h3>
      <div class="grid gap-4 lg:grid-cols-2 xl:grid-cols-3">
        {#each investor.deals as deal (deal.id)}
          <DealCard {deal} />
        {/each}
      </div>
    </div>
  {/if}
</section>
