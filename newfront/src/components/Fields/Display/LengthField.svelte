<script lang="ts">
  import type { FormField } from "$components/Fields/fields";

  type ForeignKey = {
    id: number;
    name?: string;
    username?: string;
  };

  export let formfield: FormField;
  export let value: ForeignKey;
  export let model: string;
  export let displayDeals = false;
</script>

<div class="length_field">
  <a href="#" on:click={(displayDeals = !displayDeals)}>{value.length}</a>
  {#if displayDeals}
    <div>
      {#each value as val (val.id)}
        <br /> <a href="/deal/{value.id}"> #{val.id}</a>
      {/each}
    </div>
  {/if}
</div>
