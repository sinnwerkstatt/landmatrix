<script lang="ts">
  export let extraClass = ""
</script>

<div class="rounded-lg border border-a-gray-200 bg-white p-4 {extraClass}">
  <slot />
</div>
