<script lang="ts">
  import { _ } from "svelte-i18n"
  import FacebookIcon from "$components/icons/FacebookIcon.svelte"
  import TwitterIcon from "$components/icons/TwitterIcon.svelte"
  interface MenuEntry {
    title: string
    href?: string
  }
  let menuEntries: MenuEntry[]
  $: menuEntries = [
    {
      title: $_("Data"),
      href: "/map/",
    },
    {
      title: $_("Observatories"),
      href: "/observatory/global/",
    },
    {
      title: $_("Resources"),
      href: "/resources/",
    },
    {
      title: $_("About"),
      href: "/about/the-land-matrix-initiative/",
    },
    { title: $_("FAQ"), href: "/faq/" },
    { title: $_("Contribute"), href: "/contribute/" },
    { title: $_("Data policy"), href: "/about/data-policy/" },
    { title: $_("Impressum"), href: "/about/impressum-legal-notice/" },
  ]
</script>

<div class="bg-lm-dark px-10 py-6 text-white lg:px-20 lg:py-12">
  <div class="container">
    <div class="gap-y-3 md:grid md:grid-cols-12 md:gap-x-6 xl:gap-x-12">
      <div class="heading3 col-span-12 col-start-3 text-white">
        Sign up for our eBulletin
      </div>
      <div class="col-span-2 col-start-1"><img src="/images/lm-logo-dark.png" /></div>
      <div class="col-span-8">
        <input type="text" class="h-12 w-full rounded px-3 text-black" />
      </div>
      <div class="col-span-2 col-start-11">
        <button class="button1 w-full rounded bg-orange py-[10px] px-5 text-white">
          Sign up
        </button>
      </div>
      <div class="col-span-4 mt-6">
        {#each menuEntries.slice(0, 4) as entry}
          <div class="entry">
            <a href={entry.href}>{entry.title}</a>
          </div>
        {/each}
      </div>
      <div class="col-span-4 mt-6">
        {#each menuEntries.slice(4) as entry}
          <div class="entry">
            <a href={entry.href}>{entry.title}</a>
          </div>
        {/each}
      </div>
      <div class="subtitle1 col-span-4 mt-6">
        <p>Join us</p>
        <a
          class="text-white hover:text-orange"
          target="_blank"
          rel="noreferrer"
          href="https://twitter.com/Land_Matrix"
        >
          <TwitterIcon />
        </a>
        <a
          class="ml-2 text-white hover:text-orange"
          target="_blank"
          rel="noreferrer"
          href="https://www.facebook.com/LandMatrix"
        >
          <FacebookIcon />
        </a>
      </div>
    </div>
    <p class="container mt-12">
      &copy; {new Date().getFullYear()} The Land Matrix |
      {$_("All rights reserved")}
    </p>
  </div>
</div>

<style lang="postcss">
  .entry a {
    @apply mb-3 text-white hover:text-orange;
  }
  .entry {
    @apply mb-3;
  }
</style>
