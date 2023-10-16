<script lang="ts">
  import { allColors } from "./colors.js"

  export let tileColor = ""
  export let title = ""
  export let defs = ""
</script>

<div>
  <div class="h-40 w-40 rounded-lg {tileColor}" />
  <div class="mt-3">
    <b>{title}</b>
    <ul>
      {#each allColors[defs] ?? [] as def}
        <li>{def}</li>
      {/each}
    </ul>
  </div>
</div>
