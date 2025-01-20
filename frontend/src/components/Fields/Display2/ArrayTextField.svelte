<script lang="ts">
  interface Props {
    value: string[]
  }

  let { value }: Props = $props()
</script>

<div class="flex flex-wrap gap-2">
  {#each value as v, i}
    <div>
      {v}{#if i !== value.length - 1},
      {/if}
    </div>
  {/each}
</div>
