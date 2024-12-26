<script lang="ts">
  import { allColors } from "./colors"

  interface Props {
    tileColor: string
    title: string
    defs: keyof typeof allColors
  }

  let { tileColor, title, defs }: Props = $props()
</script>

<div>
  <div class="h-24 w-24 rounded-lg lg:h-40 lg:w-40 {tileColor}"></div>
  <div class="mt-3 text-xs md:text-sm lg:text-base">
    <b>{title}</b>
    <ul class="">
      {#each allColors[defs] ?? [] as def}
        <li>{def}</li>
      {/each}
    </ul>
  </div>
</div>
