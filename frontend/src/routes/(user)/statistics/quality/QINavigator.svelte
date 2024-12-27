<script lang="ts">
  import type { Snippet } from "svelte"
  import { _ } from "svelte-i18n"
  import { blur } from "svelte/transition"

  import { page } from "$app/state"

  import ChevronDownIcon from "$components/icons/ChevronDownIcon.svelte"
  import LoadingSpinner from "$components/icons/LoadingSpinner.svelte"

  interface Props {
    model: "deal" | "investor"
    counts: ({ [key: string]: number } & { total: number }) | null
    activeKey: string | "total" | null
    list?: Snippet
  }

  let { model, counts, activeKey = $bindable(), list }: Props = $props()

  let qiPromise = $derived(
    page.data.apiClient
      .GET("/api/quality-indicators/")
      .then(res => ("error" in res ? Promise.reject(res.error) : res.data!)),
  )

  const formatRatio = (a: number, b: number): string => {
    const ratio = (a / b) * 100
    return Number.isNaN(ratio) ? "---" : `${ratio.toFixed(1)} %`
  }
</script>

{#await qiPromise}
  <LoadingSpinner />
{:then qualityIndicators}
  <nav>
    <div class="mb-4 grid grid-cols-12 gap-2 px-2 text-lg font-bold">
      <!--        <span>#</span>-->
      <span class="col-span-8 pl-5 lg:col-span-10">{$_("Name")}</span>
      <span class="col-span-2 lg:col-span-1">{$_("Count")}</span>
      <span class="col-span-2 lg:col-span-1">{$_("Ratio")}</span>
    </div>

    <ul
      class="flex flex-col gap-2 border-r"
      class:border-orange={model === "deal"}
      class:border-pelorous={model === "investor"}
    >
      <li class="grid grid-cols-12 gap-2 px-2 text-lg text-gray-700 dark:text-white">
        <span class="col-span-8 pl-5 lg:col-span-10">
          {model === "deal" ? $_("Public deals.") : $_("Public investors.")}
        </span>

        {#if counts}
          <span class="col-span-2 lg:col-span-1">
            {counts.total}
          </span>
        {:else}
          <LoadingSpinner />
        {/if}
      </li>
      {#each qualityIndicators[model] as qi (qi.key)}
        {@const isActive = qi.key === activeKey}

        <li
          class:border-r-4={isActive}
          class:bg-gray-50={isActive}
          class:dark:bg-gray-800={isActive}
          class:border-orange={model === "deal"}
          class:border-pelorous={model === "investor"}
          in:blur={{ delay: 300, duration: 300 }}
          out:blur={{ duration: 300 }}
        >
          <button
            class="grid w-full grid-cols-12 flex-nowrap items-center gap-2 px-2 text-left text-lg text-gray-700 hover:bg-gray-50 dark:text-white dark:hover:bg-gray-700"
            class:font-bold={isActive}
            title={qi.name}
            onclick={() => (activeKey = activeKey !== qi.key ? qi.key : null)}
          >
            <!--            <span class="font-bold">-->
            <!--              {index + 1}-->
            <!--            </span>-->
            <span class="col-span-8 lg:col-span-10">
              <ChevronDownIcon
                class="transition-duration-300 inline h-4 w-4 rounded transition-transform {isActive
                  ? 'rotate-180'
                  : ''}"
              />
              {qi.name}
            </span>

            {#if counts}
              <span class="col-span-2 lg:col-span-1">
                {counts[qi.key]}
              </span>
              <span class="col-span-2 lg:col-span-1">
                {formatRatio(counts[qi.key], counts["total"])}
              </span>
            {:else}
              <LoadingSpinner />
            {/if}
          </button>

          {#if isActive}
            <div class="w-2/3 p-4">
              {qi.description}
            </div>
            {@render list?.()}
          {/if}
        </li>
      {/each}
    </ul>
  </nav>
{:catch error}
  <div>Error: {error}</div>
{/await}
