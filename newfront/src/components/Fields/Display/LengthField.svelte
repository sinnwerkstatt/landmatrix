<script lang="ts">
  type ForeignKey = {
    id: number;
    name?: string;
    username?: string;
  };

  export let value: ForeignKey;
  export let displayDeals = false;
</script>

<div class="length_field">
  <button type="button" on:click={(displayDeals = !displayDeals)}>{value.length}</button
  >
  {#if displayDeals}
    <div>
      {#each value as val (val.id)}
        <br /> <a href="/deal/{value.id}"> #{val.id}</a>
      {/each}
    </div>
  {/if}
</div>
