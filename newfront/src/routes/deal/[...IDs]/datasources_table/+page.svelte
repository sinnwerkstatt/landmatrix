<script lang="ts">
  import { gql } from "@urql/svelte"
  import dayjs from "dayjs"
  import { onMount } from "svelte"

  import { page } from "$app/stores"

  import type { DataSource, Deal, DealVersion } from "$lib/types/deal"

  const [dealID, dealVersion] = $page.params.IDs.split("/").map(x =>
    x ? +x : undefined,
  )

  const media_url = import.meta.env.VITE_MEDIA_URL

  interface EDealVersion extends DealVersion {
    showEntry?: boolean
  }

  let deal: Deal
  async function queryDeal() {
    const { data } = await $page.data.urqlClient
      .query(
        gql`
          query ($id: Int!) {
            deal(id: $id, subset: UNFILTERED) {
              id
              versions {
                id
                deal {
                  fully_updated
                  status
                  draft_status
                  datasources
                }
                created_at
                created_by {
                  id
                  full_name
                }
                object_id
              }
            }
          }
        `,
        { id: dealID },
        { requestPolicy: "network-only" },
      )
      .toPromise()
    deal = data.deal
    console.log(data.deal)
  }

  onMount(() => queryDeal())

  function enriched_versions(deal): EDealVersion[] {
    let ret = [] as EDealVersion[]
    let prev_dses = [] as DataSource[]
    let startflagging = false
    let prev_dv: EDealVersion
    let prev_dv_shown = false
    deal.versions
      .slice()
      .reverse()
      .forEach((dv: EDealVersion) => {
        const dses = dv.deal.datasources as DataSource[]
        if (startflagging) {
          dv.showEntry = true
        }
        // if (prev_dses.length > dses.length) {
        //   startflagging = true;
        //   dv.showEntry = true;
        //   // ret.at(-1).showEntry = true;
        //
        //   // // try to map the entries
        //   // for (let [index, ds] of dses.entries()) {
        //   //   const pds = prev_dses[index];
        //   //   if (
        //   //     ds.type === pds.type &&
        //   //     ds.url === pds.url &&
        //   //     ds.date === pds.date
        //   //   ) {
        //   //     // this is fine
        //   //   } else {
        //   //     const pds2 = prev_dses[index + 1];
        //   //     ds.file_is_probably_broken = true;
        //   //     ds.file_prop = pds2.file;
        //   //     console.log({ index, ds, pds });
        //   //   }
        //   // }
        // }

        if (new Date(dv.created_at).getTime() >= new Date(2018, 1, 1).getTime()) {
          if (prev_dses.length > dses.length) {
            startflagging = true
            dv.showEntry = true
            // try to map the entries
            for (let [index, ds] of dses.entries()) {
              const pds = prev_dses[index]
              if (ds.type === pds.type && ds.url === pds.url && ds.date === pds.date) {
                // this is fine
              } else {
                const pds2 = prev_dses[index + 1]
                ds.file_is_probably_broken = true
                ds.file_prop = pds2.file
                console.log({ index, ds, pds })
              }
            }
          }
          if (prev_dv && !prev_dv_shown) {
            ret.push({ ...prev_dv })
            prev_dv_shown = true
          }
          ret.push({ ...dv })
        }

        prev_dv = dv
        prev_dses = dses
      })
    return ret
  }

  //   },

  function checkAll(arg: boolean) {
    let flops = document.querySelectorAll(".flopmenu")
    flops.forEach((e: Element) => ((e as HTMLInputElement).checked = arg))
  }

  const combined_status_fn = (
    status: number,
    draft_status: number | null,
    toString = false,
  ): string => {
    if (status === 4) return toString ? "Deleted" : "DELETED"
    if (draft_status === 1) return toString ? "Draft" : "DRAFT"
    if (draft_status === 2) return toString ? "Submitted for review" : "REVIEW"
    if (draft_status === 3) return toString ? "Submitted for activation" : "ACTIVATION"
    if (draft_status === 4) return toString ? "Rejected" : "REJECTED"
    if (draft_status === 5) return toString ? "To Delete" : "TO_DELETE"
    if ([2, 3].includes(status) && draft_status === null)
      return toString ? "Active" : "ACTIVE"
    throw Error(`Invalid status ${status} ${draft_status}`)
  }

  //

  //

  //
</script>

{#if deal}
  <div class="max-w-screen w-screen">
    <h2 class="my-6 text-xl font-bold text-green-700">Deal #{deal.id}</h2>
    <button on:click={() => checkAll(true)}>Expand all</button>
    /
    <button on:click={() => checkAll(false)}>Hide all</button>
    <div class="flex flex-row divide-x divide-black p-3">
      {#each enriched_versions(deal) as v}
        <div class="flex w-1/3 flex-col p-2">
          <input
            id="flop-{v.id}"
            type="checkbox"
            class="flopmenu"
            checked={v.showEntry}
          />
          <label for="flop-{v.id}" />
          <div class="w-26 flex-shrink-0">
            <span class="whitespace-nowrap">
              {dayjs(v.created_at).format("YYYY-MM-DD")}
            </span>
            <br />
            <a class="text-blue-400" href="/deal/{dealID}/v.id/">{v.id}</a>
            <br />
            {combined_status_fn(v.deal.status, v.deal.draft_status)}
          </div>

          {#each v.deal.datasources as ds}
            <div class="flex-shrink overflow-hidden">
              <div
                class="d-flex flex-column m-2 h-64 overflow-hidden rounded-lg p-2 {ds.file_is_probably_broken
                  ? 'bg-yellow-300'
                  : 'bg-green-200'}"
              >
                <div>id: {ds.id}</div>
                <div>type: {ds.type}</div>
                <div class="whitespace-nowrap">url: {ds.url}</div>
                <div>date: {ds.date}</div>
                <div>name: {ds.name}</div>
                <div>company: {ds.company}</div>
                <div class="whitespace-nowrap">
                  <div class:probably_broken={ds.file_is_probably_broken}>
                    file:
                    <a href="{media_url}{ds.file}">
                      {ds.file && ds.file.replace("uploads/", "")}
                    </a>
                  </div>
                </div>
              </div>
            </div>
          {/each}
        </div>
      {/each}
    </div>
  </div>
{/if}

<style>
  .probably_broken {
    @apply font-bold text-red-600;
  }
  .flopmenu {
    @apply invisible;
  }
  .flopmenu ~ div {
    @apply w-4;
    transition: width 50ms ease;
  }

  .flopmenu:checked ~ div {
    width: 100%;
  }
  .flopmenu + label::before {
    content: "SHOW";
    border-radius: 5px;

    padding: 0.3em 0.75em;
    background: red;
    color: white;
  }

  .flopmenu:checked + label::before {
    content: "HIDE";
    border-radius: 5px;
    padding: 0.3em 0.75em;
    background: green;
    color: white;
  }
</style>
