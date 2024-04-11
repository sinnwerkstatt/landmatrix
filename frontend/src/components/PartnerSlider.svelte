<script lang="ts">
  import {
    Splide,
    SplideSlide,
    SplideTrack,
    type Options,
  } from "@splidejs/svelte-splide"

  import type { Partner } from "$lib/types/wagtail"

  import "@splidejs/svelte-splide/css"

  export let perPage: number
  export let partners: Partner[]

  let options: Options
  $: options = {
    type: "loop",
    interval: 3000,
    perMove: 1,
    pagination: false,
    pauseOnHover: false,
    pauseOnFocus: false,
    autoplay: partners.length > perPage,
    perPage: Math.min(partners.length, perPage),
    drag: partners.length > perPage,
    arrows: partners.length > perPage,
    breakpoints: {
      640: {
        // 'sm'
        autoplay: partners.length > 2,
        perPage: Math.min(partners.length, 2),
        drag: partners.length > 2,
        arrows: false,
      },
      1024: {
        // 'lg'
        autoplay: partners.length > 3,
        perPage: Math.min(partners.length, 3),
        drag: partners.length > 3,
        arrows: partners.length > 3,
      },
    },
    classes: {
      arrow: "splide__arrow no-background",
    },
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

<!-- TODO nuts maybe we have to reenable this. -->
<!--<style lang="postcss">-->
<!--  :global(.no-background) {-->
<!--    @apply bg-transparent hover:bg-orange;-->
<!--  }-->
<!--</style>-->
