<script lang="ts">
  import { onDestroy, onMount } from "svelte"
  import { expoOut } from "svelte/easing"
  import { tweened } from "svelte/motion"

  import { contentRootElement } from "$lib/stores/basics"

  export let value: {
    deals: number
    text: string
    text_below: string
  }

  const progress = tweened(0, { duration: 3000, easing: expoOut })

  let countElement: HTMLElement
  let intersectionObserver: IntersectionObserver
  onMount(async () => {
    intersectionObserver = new IntersectionObserver(
      entries => {
        if (entries[0].isIntersecting) progress.set(value.deals)
      },
      { root: $contentRootElement, threshold: 0.7 },
    )
    intersectionObserver.observe(countElement)
  })
  onDestroy(() => {
    if (intersectionObserver) intersectionObserver.disconnect()
  })
</script>

<div
  class="content-fit container mx-auto my-20 bg-[url('/images/Background_hoehenlinien.png')] bg-contain p-6 text-center dark:bg-[url('/images/Background_hoehenlinien_dark.png')]"
>
  <h3 class="heading1 dark:text-white">{value.text}</h3>
  <p class="display1 text-pelorous" bind:this={countElement}>
    {Math.round($progress).toLocaleString("fr").replace(",", ".")}
  </p>
  <p class="heading2 text-pelorous-300">
    {value.text_below}
  </p>
</div>
