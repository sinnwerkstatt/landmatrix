<script lang="ts">
  import { _ } from "svelte-i18n"

  import { type InvestorHull } from "$lib/types/data"

  import DealCard from "./DealCard.svelte"
  import InvestorCard from "./InvestorCard.svelte"

  export let investor: InvestorHull
</script>

<section>
  <div class="mb-16 mt-2 space-y-4">
    <h3 class="heading4 my-0">
      {$_("Children (Involvements as parent)")} ({investor.children.length})
    </h3>
    <div class="grid gap-4 lg:grid-cols-2 xl:grid-cols-3">
      {#each investor.children as involvement}
        <InvestorCard {involvement} />
      {/each}
    </div>
  </div>

  <div class="mb-16 mt-2 space-y-4">
    <h3 class="heading4 my-0">
      {$_("Parents (Involvements as child)")} ({investor.parents.length})
    </h3>
    <div class="grid gap-4 lg:grid-cols-2 xl:grid-cols-3">
      {#each investor.parents as involvement}
        <InvestorCard isParent {involvement} />
      {/each}
    </div>
  </div>
</section>

{#if investor.deals.length > 0}
  <section>
    <div class="mb-10 mt-2 space-y-4">
      <h3 class="heading4 my-0">
        {$_("Deals (Involvements as Operating company)")} ({investor.deals.length})
      </h3>
      <div class="grid gap-4 lg:grid-cols-2 xl:grid-cols-3">
        {#each investor.deals as deal}
          <DealCard {deal} />
        {/each}
      </div>
    </div>
  </section>
{/if}
