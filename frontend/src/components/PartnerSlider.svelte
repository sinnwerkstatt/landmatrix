<script lang="ts">
  import { Splide, SplideSlide, SplideTrack } from "@splidejs/svelte-splide"

  import type { Partner } from "$lib/types/wagtail"

  import "@splidejs/svelte-splide/css/core"

  export let perPage: number
  export let partners: Partner[]

  const options = {
    autoplay: partners.length > perPage,
    perPage: Math.min(partners.length, perPage),
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
          <a
            class="mx-auto flex h-[150px] w-[150px] items-center justify-center"
            href={partner.homepage}
            title={partner.name}
            target="_blank"
          >
            <img
              class="mx-auto bg-gray-50"
              height="150"
              width="150"
              src={partner.logo}
              alt={partner.name}
            />
          </a>
        </SplideSlide>
      {/each}
    </SplideTrack>
  </Splide>
</div>
