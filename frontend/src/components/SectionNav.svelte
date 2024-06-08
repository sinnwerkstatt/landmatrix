<script lang="ts">
  import { page } from "$app/stores"

  export let sections: { slug: string; label: string }[]
  export let baseUrl: string
</script>

<nav
  class="z-100 border-b border-orange bg-white px-4 py-2 lg:border-b-0 lg:border-r lg:px-0 dark:bg-gray-900"
>
  <!--  <h3 class="heading5">{$_("Sections")}</h3>-->
  <ol
    class="flex flex-wrap justify-center gap-x-4 gap-y-2 overflow-x-auto lg:flex-col lg:gap-4"
  >
    {#each sections as { slug, label }}
      {@const href = `${baseUrl}/${slug}/`}
      {@const isActive = href === $page.url.pathname}

      <li
        class="border-orange lg:text-left {isActive
          ? 'border-b-4 lg:border-b-0 lg:border-r-4'
          : ''}"
      >
        {#if label}
          <a {href} class={isActive ? "text-gray-700 dark:text-white" : ""}>
            {label}
          </a>
        {:else}
          <hr />
        {/if}
      </li>
    {/each}
  </ol>
</nav>
