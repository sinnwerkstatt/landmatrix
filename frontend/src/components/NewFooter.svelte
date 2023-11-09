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

<div class="bg-lm-dark px-10 py-12 text-white lg:px-20">
  <div class="container mx-auto">
    <!--    Newsletter-->
    <div class="items-end gap-6 lg:flex">
      <div class="max-w-[200px]">
        <img src="/images/lm-logo-dark.png" />
      </div>
      <div class="w-full grow sm:flex sm:items-end sm:gap-6">
        <div class="grow">
          <h3 class="heading3 text-white">Sign up for our eBulletin</h3>
          <input type="text" class="my-3 h-12 w-full rounded px-3 text-black sm:my-0" />
        </div>
        <div class="sm:w-1/3 lg:w-1/4 xl:w-1/6">
          <button
            class="button1 h-12 w-full rounded bg-orange px-5 py-[10px] text-white transition hover:bg-orange-600"
          >
            Sign up
          </button>
        </div>
      </div>
    </div>
    <hr class="my-10 text-white lg:hidden" />
    <!--    Menu-->
    <div class="w-full lg:mt-6 lg:grid lg:grid-cols-3">
      <div class="my-6">
        {#each menuEntries.slice(0, 4) as entry}
          <div class="entry">
            <a href={entry.href}>{entry.title}</a>
          </div>
        {/each}
      </div>

      <div class="mt-6">
        {#each menuEntries.slice(4) as entry}
          <div class="entry">
            <a href={entry.href}>{entry.title}</a>
          </div>
        {/each}
      </div>
      <div class="subtitle1 mt-6">
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
