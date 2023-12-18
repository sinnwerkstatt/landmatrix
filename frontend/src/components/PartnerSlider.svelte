<script lang="ts">
  import { Splide, SplideSlide, SplideTrack } from "@splidejs/svelte-splide"

  import "@splidejs/svelte-splide/css/core"

  import type { Partner } from "$lib/types/wagtail"

  export let countSlides: number
  export let partners: Partner[]
  export let bw = true

  const options = {
    autoplay: true,
    perPage: countSlides,
    perMove: 1,
    type: "loop",
    arrows: false,
    pagination: false,
    pauseOnHover: false,
    pauseOnFocus: false,
    interval: 3000,
  }
</script>

<div class="container mx-auto mb-12">
  <Splide hasTrack={false} {options}>
    <SplideTrack>
      {#each partners as partner}
        <SplideSlide>
          <div class="mx-auto max-w-[360px] px-6">
            <a href={partner.homepage} target="_blank">
              <img src={partner.logo} alt={partner.name} class="mx-auto" />
            </a>
          </div>
        </SplideSlide>
      {/each}
    </SplideTrack>
  </Splide>
</div>
