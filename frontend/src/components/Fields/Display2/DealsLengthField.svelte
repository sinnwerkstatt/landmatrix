<script lang="ts">
  export let value: number[] = []
</script>

{#if value.length}
  <details class="whitespace-nowrap" data-fieldname="investor.deals">
    <summary class="cursor-pointer text-orange hover:underline">
      {value.length}
    </summary>
    <ul class="flex flex-col">
      {#each value as val}
        <li><a href="/deal/{val}/">#{val}</a></li>
      {/each}
    </ul>
  </details>
{/if}

<style>
  details > summary {
    list-style: none;
  }

  details > summary::-webkit-details-marker {
    display: none;
  }
</style>
