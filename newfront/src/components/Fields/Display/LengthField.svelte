<script lang="ts">
  type ForeignKey = {
    id: number;
    name?: string;
    username?: string;
  };

  export let value: ForeignKey[];
  export let displayDeals = false;
</script>

<div class="length_field">
  {#if value.length > 0}
    <button
      class="text-orange"
      type="button"
      on:click={() => (displayDeals = !displayDeals)}
    >
      {value.length}
    </button>
    {#if displayDeals}
      <ul>
        {#each value as val (val.id)}
          <li><a href="/deal/{value.id}"> #{val.id}</a></li>
        {/each}
      </ul>
    {/if}
  {/if}
</div>
