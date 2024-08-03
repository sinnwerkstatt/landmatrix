<script lang="ts">
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import { type InvestorHull } from "$lib/types/data"
  import { isReporterOrAbove } from "$lib/utils/permissions"

  import DealCard from "./DealCard.svelte"
  import InvestorCard from "./InvestorCard.svelte"

  export let investor: InvestorHull

  $: involvements = investor.involvements.filter(
    i =>
      // FIXME: make sure other_investor is always defined (in backend)
      !!i.other_investor &&
      // FIXME: apply visibility filters in backend
      (isReporterOrAbove($page.data.user) ||
        !(i.other_investor.deleted || i.other_investor.draft_only)),
  )

  $: involvementsAsParent = involvements.filter(
    i => investor.id === i.parent_investor_id,
  )
  $: involvementsAsChild = involvements.filter(i => investor.id === i.child_investor_id)
</script>

<section>
  <div class="mb-16 mt-2 space-y-4">
    <h3 class="heading4 my-0">
      {$_("Children (Involvements as parent)")} ({involvementsAsParent.length})
    </h3>
    <div class="grid gap-4 lg:grid-cols-2 xl:grid-cols-3">
      {#each involvementsAsParent as involvement}
        <InvestorCard {involvement} />
      {/each}
    </div>
  </div>

  <div class="mb-16 mt-2 space-y-4">
    <h3 class="heading4 my-0">
      {$_("Parents (Involvements as child)")} ({involvementsAsChild.length})
    </h3>
    <div class="grid gap-4 lg:grid-cols-2 xl:grid-cols-3">
      {#each involvementsAsChild as involvement}
        <InvestorCard {involvement} />
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
