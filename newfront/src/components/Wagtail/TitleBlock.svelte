<script lang="ts">
  export let value: {
    url?: string;
    value: string;
    fa_icon: string;
  };
</script>

<template>
  <h3>
    {#if value.url}
      <a href={value.url}>
        <i class="fa fa-{value.fa_icon}" />
        {value.value}
      </a>
    {:else}
      <i class="fa fa-{value.fa_icon}" /> {value.value}
    {/if}
  </h3>
</template>
