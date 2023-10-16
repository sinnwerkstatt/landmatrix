<script lang="ts">
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import NavDropDown from "$components/Navbar/NavDropDown.svelte"

  let dataViews: { title: string; route: string }[]
  $: dataViews = [
    {
      title: $_("Deals"),
      route: "/list/deals/",
    },
    {
      title: $_("Investors"),
      route: "/list/investors/",
    },
  ]

  let chartViews: { title: string; route: string }[]
  $: chartViews = [
    {
      title: $_("Web of transnational deals"),
      route: "/charts/web-of-transnational-deals/",
    },
    {
      title: $_("Global Map of Investments"),
      route: "/charts/global-map-of-investments/",
    },
    {
      title: $_("Dynamics overview"),
      route: "/charts/dynamics-overview/",
    },
    {
      title: $_("Produce info map"),
      route: "/charts/produce-info/",
    },
    {
      title: $_("Country profiles"),
      route: "/charts/country-profiles/",
    },
  ]
</script>

<div
  class="pointer-events-none absolute inset-x-0 top-3 z-30 mx-auto text-center drop-shadow"
>
  <nav id="data-navigation">
    <ul
      class="pointer-events-auto inline-flex items-center border border-orange bg-white text-left drop-shadow dark:bg-gray-800"
    >
      <li>
        <a
          href="/map/"
          class="nav-link"
          class:active={$page.url.pathname.startsWith("/map")}
        >
          {$_("Map")}
        </a>
      </li>
      <NavDropDown>
        <svelte:fragment slot="title">
          <span class="capitalize">{$_("Data")}</span>
        </svelte:fragment>
        <ul class="border-2 border-orange bg-white dark:bg-gray-800">
          {#each dataViews as view}
            <li class="whitespace-nowrap">
              <a
                href={view.route}
                class="nav-link"
                class:active={$page.url.pathname.startsWith(view.route)}
              >
                {view.title}
              </a>
            </li>
          {/each}
        </ul>
      </NavDropDown>
      <NavDropDown>
        <svelte:fragment slot="title">
          <span class="capitalize">{$_("Charts")}</span>
        </svelte:fragment>
        <ul class="border-2 border-orange bg-white dark:bg-gray-800">
          {#each chartViews as view}
            <li class="whitespace-nowrap">
              <a
                href={view.route}
                class="nav-link"
                class:active={$page.url.pathname.startsWith(view.route)}
              >
                {view.title}
              </a>
            </li>
          {/each}
        </ul>
      </NavDropDown>
    </ul>
  </nav>
</div>
