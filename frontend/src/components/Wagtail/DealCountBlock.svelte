<script lang="ts">
  import { onMount } from "svelte"
  import { expoOut } from "svelte/easing"
  import { tweened } from "svelte/motion"

  import { contentRootElement } from "$lib/stores"

  export let value: {
    deals: number
    text: string
    text_below: string
  }

  let element: HTMLElement
  let countElement: HTMLElement
  const progress = tweened(0, { duration: 3000, easing: expoOut })
  let countElementInWindow = false
  $: countElementInWindow

  async function checkPosition() {
    if (countElementInWindow) {
      await progress.set(value.deals)
    } else setTimeout(() => checkPosition().then(), 3000)
  }
  async function setProgress() {
    await progress.set(value.deals)
    setTimeout(() => setProgress(), 3000)
  }

  onMount(async () => {
    checkPosition().then()

    $contentRootElement.addEventListener("scroll", () => {
      countElementInWindow =
        countElement?.getBoundingClientRect().bottom < window.innerHeight

      if (countElementInWindow) {
        setProgress()
      }
    })
  })
</script>

<div
  class="content-fit container mx-auto my-20 bg-[url('/images/Background_hoehenlinien.png')] bg-contain p-6 text-center dark:bg-[url('/images/Background_hoehenlinien_dark.png')]"
  bind:this={element}
>
  <h3 class="heading1 dark:text-white">{value.text}</h3>
  <p class="display1 text-pelorous" bind:this={countElement}>
    {Math.round($progress).toLocaleString("fr").replace(",", ".")}
  </p>
  <p class="heading2 text-pelorous-300">
    {value.text_below}
  </p>
</div>
