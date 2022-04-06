<script lang="ts">
  import type { FormField } from "$components/Fields/fields";

  export let formfield: FormField;
  export let value: object[];
  export let model: string;

  export let displayDeals = false;
  // const data = () => {
  //     return {
  //       displayDeals: false,
  //     };
  //   }
</script>

<div class="length_field">
  <a href="#" on:click={(displayDeals = !displayDeals)}>{value.length}</a>
  {#if displayDeals}
    <div>
      {#each value as val (val.id)}
        <br /> <a href="/deal/{val.id}"> #{val.id}</a>
      {/each}
    </div>
  {/if}
</div>
