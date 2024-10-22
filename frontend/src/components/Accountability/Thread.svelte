<script lang="ts">
  import ThreadItem from "./atomic/ThreadItem.svelte"

  const data1 = {
    user: { name: "Jérémy", initials: "JB" },
    type: "score",
    deal: 1235,
    variable: 1,
    score: "waiting",
    timestamp: "2024-05-13T14:48:00.000+09:00",
  }

  const data2 = {
    user: { name: "Angela", initials: "AH" },
    type: "score",
    deal: 1235,
    variable: 6,
    score: "validated",
    timestamp: "2024-05-12T14:48:00.000+09:00",
    comment: "I'm not sure about this one, can anybody please check?",
  }

  const data3 = {
    user: { name: "Marie", initials: "MG" },
    type: "score",
    deal: 1237,
    variable: 3,
    score: "waiting",
    timestamp: "2024-05-10T14:48:00.000+09:00",
  }

  const items = [data1, data2, data3]
</script>

<div class="">
  <h2 class="mb-6 text-a-2xl font-semibold">Activity thread</h2>

  <div class="flex flex-col">
    {#each items as data, i}
      {@const line = i + 1 == items.length ? false : true}
      <ThreadItem {data} {line} />
    {/each}
  </div>
</div>
