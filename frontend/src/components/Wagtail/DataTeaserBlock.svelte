<script lang="ts">
  import CakeTeaser from "$components/Data/Charts/CakeTeaser.svelte"
  import MapTeaser from "$components/Data/MapTeaser.svelte"
  import TableTeaser from "$components/Data/TableTeaser.svelte"

  export let value: {
    title: string
    subtitle: string
    cards: {
      title: string
      teaser: string
      link: {
        text: string
        href: string
      }
    }[]
  }
</script>

<div class="container mx-auto my-20 px-10 py-6">
  <h2 class="caption text-center lg:text-left dark:text-white">{value.title}</h2>
  <h3
    class="heading2 mb-10 text-center underline lg:w-1/2 lg:text-left dark:text-white"
  >
    {value.subtitle}
  </h3>

  <div data-block="data_teaser" class="md:grid md:grid-cols-3 lg:grid-cols-3 lg:gap-24">
    <div class="mx-auto mb-20 text-center md:mb-0">
      <MapTeaser />
      <h3 class="heading2 dark:text-white">{value.cards[0].title}</h3>
      <p class="body1 mx-auto">{value.cards[0].teaser}</p>
      <a class="butn-link butn-secondary" href={value.cards[0].link.href}>
        {value.cards[0].link.text}
      </a>
    </div>
    <div class="mx-auto mb-20 text-center md:mb-0">
      <CakeTeaser />
      <h3 class="heading2 dark:text-white">{value.cards[1].title}</h3>
      <p class="body1 mx-auto">{value.cards[1].teaser}</p>
      <a class="butn-link butn-secondary" href={value.cards[1].link.href}>
        {value.cards[1].link.text}
      </a>
    </div>
    <div class="mx-auto mb-20 text-center md:mb-0">
      <TableTeaser />
      <h3 class="heading2 dark:text-white">{value.cards[2].title}</h3>
      <p class="body1 mx-auto">{value.cards[2].teaser}</p>
      <a class="butn-link butn-secondary" href={value.cards[2].link.href}>
        {value.cards[2].link.text}
      </a>
    </div>
  </div>
</div>
