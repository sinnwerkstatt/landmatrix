<script lang="ts">
  import CardKPI from "$components/Accountability/CardKPI.svelte"
  import Thread from "$components/Accountability/Thread.svelte"

  const totalDeals = 130
  const toScore = 100
  const waiting = 20
  const validated = 100
</script>

<div class="">
  <!-- <p>Project ID: {$page.params.project}</p> -->

  <!-- KPI cards -->
  <div class="flex flex-col gap-4 xl:grid xl:grid-cols-3">
    <CardKPI
      label="To score"
      value="{toScore}/{totalDeals}"
      color="neutral"
      icon="check"
      button="Go to"
    />
    <CardKPI
      label="Waiting for review"
      value="{waiting}/{totalDeals}"
      color="orange"
      icon="eye"
      button="Go to"
    />
    <CardKPI
      label="Validated"
      value="{validated}/{totalDeals}"
      color="green"
      icon="check"
      button="Go to"
    />
  </div>

  <!-- Map -->
  <div class="mb-8 mt-4 grid h-80 place-items-center rounded-lg bg-a-gray-100">
    <span class="text-a-gray-400">Map placeholder</span>
  </div>

  <!-- Activity thread -->
  <Thread />
</div>
