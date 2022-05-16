<script lang="ts">
  import { _ } from "svelte-i18n";
  import { page } from "$app/stores";
  import NavDropDown from "$components/LowLevel/NavDropDown.svelte";

  const label = { deals: $_("Deals"), investors: $_("Investors") };
  const chartEntries = [
    {
      title: $_("Web of transnational deals"),
      route: "/charts/web-of-transnational-deals",
    },
    { title: $_("Dynamics overview"), route: "/charts/dynamics-overview" },
    { title: $_("Produce info map"), route: "/charts/produce-info" },
    { title: $_("Country profiles"), route: "/charts/country-profiles" },
  ];

  console.log($page.url.pathname);
  $: dataItemName = {};
</script>

<div class="absolute mx-auto top-3 inset-x-0 text-center z-30 drop-shadow">
  <nav id="data-navigation">
    <ul class="inline-flex drop-shadow bg-white text-left">
      <li>
        <a
          href="/map"
          class="nav-link"
          class:active={$page.url.pathname.startsWith("/map")}
        >
          {$_("Map")}
        </a>
      </li>
      <NavDropDown
        title={$_("Table")}
        class={$page.url.pathname.startsWith("/list") ? "bg-orange text-white" : ""}
      >
        <ul class="border border-orange bg-white">
          {#if dataItemName !== label.deals}
            <li>
              <a href="/list/deals" class="nav-link">
                {label.deals}
              </a>
            </li>
          {/if}
          {#if dataItemName !== label.investors}
            <li>
              <a href="/list/investors" class="nav-link">
                {label.investors}
              </a>
            </li>
          {/if}
        </ul>
      </NavDropDown>

      <NavDropDown
        title={$_("Charts")}
        class={$page.url.pathname.startsWith("/charts") ? "bg-orange text-white" : ""}
      >
        <ul class="border border-orange bg-white">
          {#each chartEntries as entry}
            <li class="whitespace-nowrap">
              <a href={entry.route} class="nav-link">
                {entry.title}
              </a>
            </li>
          {/each}
        </ul>
      </NavDropDown>
    </ul>
  </nav>
</div>
