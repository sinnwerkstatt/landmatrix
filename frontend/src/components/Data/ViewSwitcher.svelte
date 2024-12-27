<script lang="ts">
  import { env } from "$env/dynamic/public"
  import { _ } from "svelte-i18n"

  import { page } from "$app/state"

  import NavDropDown from "$components/Navbar/NavDropDown.svelte"

  const showAllCharts = !!env.PUBLIC_FF_DISPLAY_ALL_CHARTS

  let dataViews: { title: string; route: string }[] = $derived([
    {
      title: $_("Deals"),
      route: "/list/deals/",
    },
    {
      title: $_("Investors"),
      route: "/list/investors/",
    },
  ])

  let chartViews: { title: string; route: string }[] = $derived.by(() => {
    let _chartViews = [
      {
        title: $_("Web of transnational deals"),
        route: "/charts/web-of-transnational-deals/",
      },
      {
        title: $_("Dynamics overview"),
        route: "/charts/dynamics-overview/",
      },
      {
        title: $_("Produce info map"),
        route: "/charts/produce-info/",
      },
    ]
    if (showAllCharts) {
      return [
        ..._chartViews,
        {
          title: $_("Global map of Investments"),
          route: "/charts/global-map-of-investments/",
        },
      ]
    }
    return _chartViews
  })

  let countryProfileViews: { title: string; route: string }[] = $derived.by(() => {
    let _countryProfileViews = [
      {
        title: $_("LSLA by negotiation status"),
        route: "/country-profile/lsla/",
      },
      {
        title: $_("Dynamics of deal by investor type"),
        route: "/country-profile/dynamics-of-deal/",
      },
      {
        title: $_("Number of intentions per category of production"),
        route: "/country-profile/intentions-of-investments/",
      },
      {
        title: $_("Concluded deals over time"),
        route: "/country-profile/concluded-deals-over-time/",
      },
    ]

    if (showAllCharts)
      return [
        {
          title: $_("Land acquisitions by category of production"),
          route: "/country-profile/land-acquisitions/",
        },
        ..._countryProfileViews,
      ]

    return _countryProfileViews
  })
</script>

<div
  class="pointer-events-none absolute inset-x-0 top-3 z-30 mx-auto text-center drop-shadow"
>
  <nav id="data-navigation">
    <ul
      class="pointer-events-auto inline-flex items-center border-2 border-orange bg-white text-left dark:bg-gray-900"
    >
      <li>
        <a
          href="/map/"
          class="nav-link-main"
          class:active={page.url.pathname.startsWith("/map/")}
        >
          {$_("Map")}
        </a>
      </li>
      <li>
        <NavDropDown>
          {#snippet title()}
            <span
              class="nav-link-main"
              class:active={page.url.pathname.startsWith("/list/")}
            >
              {$_("Tables")}
            </span>
          {/snippet}

          <ul class="border border-orange-500">
            {#each dataViews as view}
              <li class="whitespace-nowrap">
                <a
                  href={view.route}
                  class="nav-link-secondary bg-white dark:bg-gray-900"
                  class:active={page.url.pathname.startsWith(view.route)}
                >
                  {view.title}
                </a>
              </li>
            {/each}
          </ul>
        </NavDropDown>
      </li>
      <li>
        <NavDropDown>
          {#snippet title()}
            <span
              class="nav-link-main"
              class:active={["/charts/", "/country-profile/"].some(path =>
                page.url.pathname.startsWith(path),
              )}
            >
              {$_("Charts")}
            </span>
          {/snippet}
          <ul class="border border-orange bg-white dark:bg-gray-800">
            {#each chartViews as view}
              <li class="whitespace-nowrap">
                <a
                  href={view.route}
                  class="nav-link-secondary bg-white dark:bg-gray-900"
                  class:active={page.url.pathname.startsWith(view.route)}
                >
                  {view.title}
                </a>
              </li>
            {/each}
            {#each countryProfileViews as view}
              <li class="whitespace-nowrap">
                <a
                  href={view.route}
                  class="nav-link-secondary bg-white dark:bg-gray-900"
                  class:active={page.url.pathname.startsWith(view.route)}
                >
                  {view.title}
                </a>
              </li>
            {/each}
          </ul>
        </NavDropDown>
      </li>
    </ul>
  </nav>
</div>
