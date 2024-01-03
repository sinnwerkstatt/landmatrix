<script lang="ts">
  export let title = ""
</script>

<div class="mt-2 space-y-4 pt-6">
  {#if title}
    <h3 class="heading3 my-0">{title}</h3>
  {/if}

  <slot />
</div>
