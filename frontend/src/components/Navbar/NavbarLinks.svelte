<script lang="ts">
  import { _ } from "svelte-i18n"

  import { blogCategories } from "$lib/stores"
  import { aboutPages, observatoryPages } from "$lib/stores/wagtail"

  import SubEntries from "$components/Navbar/SubEntries.svelte"

  interface SubMenu {
    title: string
    subEntries: {
      title: string
      href: string
    }[]
    href?: never
  }

  let menuEntries: SubMenu[] = []
  $: menuEntries = [
    {
      title: $_("Data"),
      subEntries: [
        { title: $_("Map"), href: "/map/" },
        { title: $_("Tables"), href: "/list/" },
        { title: $_("Charts"), href: "/charts/" },
      ],
    },
    {
      title: $_("Observatories"),
      subEntries: $observatoryPages.map(page => ({
        title: page.title,
        href: `/observatory/${page.meta.slug}/`,
      })),
    },
    {
      title: $_("Resources"),
      subEntries: [
        { title: $_("All"), href: "/resources/" },
        ...$blogCategories.map(cat => ({
          title: cat.name,
          href: `/resources/?category=${cat.slug}`,
        })),
      ],
    },
    {
      title: $_("About"),
      subEntries: $aboutPages.map(page => ({
        title: page.title,
        href: `/about/${page.meta.slug}/`,
      })),
    },
  ]

  export let showMenu: boolean
</script>

<ul
  class="mx-3 mb-2 w-full items-center justify-evenly gap-4 divide-y lg:flex lg:h-16 lg:divide-y-0 xl:gap-5"
>
  {#each menuEntries as entry}
    <SubEntries
      title={entry.title}
      subEntries={entry.subEntries}
      on:close={() => (showMenu = false)}
    />
  {/each}
  <li class=" py-1">
    <a class="nav-link-main" href="/faq/" on:click={() => (showMenu = false)}>
      {$_("FAQ")}
    </a>
  </li>
  <li class="py-1">
    <a class="nav-link-main" href="/contribute/" on:click={() => (showMenu = false)}>
      {$_("Contribute")}
    </a>
  </li>
</ul>
