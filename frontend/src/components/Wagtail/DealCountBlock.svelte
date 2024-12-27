<script lang="ts">
  import { onDestroy, onMount } from "svelte"
  import { expoOut } from "svelte/easing"
  import { Tween } from "svelte/motion"

  interface Props {
    value: {
      deals: number
      text: string
      text_below: string
    }
  }

  let { value }: Props = $props()

  const progress = new Tween(0, { duration: 3000, easing: expoOut })

  let countElement: HTMLElement | undefined = $state()
  let intersectionObserver: IntersectionObserver
  onMount(async () => {
    intersectionObserver = new IntersectionObserver(
      entries => {
        if (entries[0].isIntersecting) progress.set(value.deals)
      },
      { threshold: 0.7 },
    )
    if (countElement) intersectionObserver.observe(countElement)
  })
  onDestroy(() => {
    if (intersectionObserver) intersectionObserver.disconnect()
  })
</script>

<div
  class="container mx-auto my-20 bg-[url('/images/Background_hoehenlinien.png')] bg-cover bg-center p-6 text-center dark:bg-[url('/images/Background_hoehenlinien_dark.png')]"
>
  <h3 class="heading1 dark:text-white">{value.text}</h3>
  <p class="display1 text-pelorous" bind:this={countElement}>
    {Math.round(progress.current).toLocaleString("fr").replace(",", ".")}
  </p>
  <p class="heading2 text-pelorous-300">
    {value.text_below}
  </p>
</div>
