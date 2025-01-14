<script lang="ts">
  import { dealFields } from "$lib/fieldLookups"

  import Badge from "./Badge.svelte"

  interface Props {
    // export let dealInfo:{label:string, value:string}[]
    deal?:
      | {
          id: number
          country: { id: number; name: string }
          deal_size: number
          operating_company: { id: number; name: string }
        }
      | undefined
    fields: string[]
    main_info?: boolean
  }

  let { deal = undefined, fields, main_info = false }: Props = $props()
</script>

{#if deal}
  <div class="flex flex-col divide-y rounded-lg border px-4">
    {#if main_info}
      <div class="row">
        <div>Country</div>
        <div class="font-normal text-a-gray-500">{deal.country.name}</div>
      </div>
      <div class="row">
        <div>Deal size</div>
        <div class="font-normal text-a-gray-500">{deal.deal_size} ha</div>
      </div>
      <div class="row">
        <div>Investor</div>
        <div>
          {#if deal.operating_company.id}
            <span class="flex gap-4">
              {deal.operating_company.id}
              <Badge
                label={deal.operating_company.id}
                color="blue"
                variant="filled"
                href="https://landmatrix.org/investor/{deal.operating_company.id}/"
              ></Badge>
            </span>
          {:else}
            <span class="font-normal text-a-gray-500">—</span>
          {/if}
        </div>
      </div>
    {:else}
      {#each fields as field}
        {@const value = deal[field]}
        {@const label = $dealFields[field]?.label ?? field}
        <div class="row">
          <div>{label}</div>
          <div class="font-normal text-a-gray-500">
            <!-- TODO: Parse arrays and objects properly -->
            {#if value && value.length > 0}
              {#if Array.isArray(value)}
                {value.join(", ")}
              {:else}
                {value}
              {/if}
            {:else}
              —
            {/if}
          </div>
        </div>
      {/each}
    {/if}
  </div>
{/if}

<style>
  .row {
    @apply py-2;
    @apply grid gap-4;
    grid-template-columns: 24rem auto;
  }
</style>
