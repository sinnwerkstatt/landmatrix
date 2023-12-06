<script lang="ts">
  export let title = ""

  export let fields: unknown[] = []

  function isEmpty(field: unknown): boolean {
    // console.log(field)
    if (field === undefined || field === null || field === "") return false
    if (Array.isArray(field) && field.length === 0) return false
    return true
  }
</script>

{#if fields.filter(isEmpty).length > 0}
  <div class="mt-2 space-y-4">
    <h3 class="heading3 my-0">{title}</h3>

    <slot />
  </div>
{/if}
