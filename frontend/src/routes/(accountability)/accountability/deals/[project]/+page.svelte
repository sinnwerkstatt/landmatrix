<script lang="ts">
  import { deals, loadingDeals } from "$lib/accountability/stores"

  import CardKPI from "$components/Accountability/CardKPI.svelte"
  import Thread from "$components/Accountability/Thread.svelte"

  // const totalDeals = 130
  // const toScore = 100
  // const waiting = 20
  // const validated = 100
</script>

<div class="">
  <!-- <p>Project ID: {$page.params.project}</p> -->

  <!-- KPI cards -->
  <div class="flex flex-col gap-4 xl:grid xl:grid-cols-3">
    <CardKPI
      label="Number of deals"
      value={$deals.length}
      color="neutral"
      icon="check"
      button=""
      loader={$loadingDeals}
    />
    <CardKPI
      label="Waiting for review"
      value="…"
      color="orange"
      icon="eye"
      button=""
      loader={$loadingDeals}
    />
    <CardKPI
      label="Validated"
      value="…"
      color="green"
      icon="check"
      button=""
      loader={$loadingDeals}
    />
  </div>

  <!-- Map -->
  <div class="mb-8 mt-4 grid h-80 place-items-center rounded-lg bg-a-gray-100">
    <span class="text-a-gray-400">Map placeholder</span>
  </div>

  <!-- Activity thread -->
  <Thread />
</div>
