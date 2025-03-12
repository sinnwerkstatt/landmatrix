<script lang="ts">
  import { diff } from "deep-object-diff"
  import { _ } from "svelte-i18n"
  import type { Writable } from "svelte/store"

  import { dealFields, investorFields } from "$lib/fieldLookups"
  import { getTypedKeys } from "$lib/helpers.js"
  import type {
    DealHull,
    FieldQuotations,
    InvestorHull,
    Model,
    MutableDealHull,
    MutableInvestorHull,
    Quotations,
    SubmodelQuotations,
  } from "$lib/types/data"

  import { getMutableObject } from "$components/Data/stores"
  import CheckIcon from "$components/icons/CheckIcon.svelte"
  import XIcon from "$components/icons/XIcon.svelte"
  import Modal from "$components/Modal.svelte"
  import ChangedFieldItem from "$components/Quotations/ChangedFieldItem.svelte"
  import DataSourceList from "$components/Quotations/DataSourceList.svelte"
  import {
    clearSelected,
    toggleSelected,
  } from "$components/Quotations/selectedPaths.svelte"
  import SubModelDiff from "$components/Quotations/SubModelDiff.svelte"
  import { mergeKeys } from "$components/Quotations/utils"

  interface Props {
    open: boolean
    model?: Model
    oldObject: DealHull | InvestorHull
    newObject: Writable<MutableDealHull | MutableInvestorHull>
    onclick?: () => void
  }

  let {
    open = $bindable(),
    model = "deal",
    oldObject,
    newObject,
    onclick,
  }: Props = $props()

  const getRichField = (fieldname: string) =>
    (model === "deal" ? $dealFields : $investorFields)[fieldname]

  const mutableObj = getMutableObject(model)

  const SUBMODEL_LABELS = $derived({
    locations: $_("Location"),
    contracts: $_("Contract"),
    datasources: $_("Data Source"),
    involvements: $_("Involvement"),
  })
  type SubmodelKey = keyof typeof SUBMODEL_LABELS
  const submodelKeys = $derived(getTypedKeys(SUBMODEL_LABELS))

  const jsonKeys = $derived(
    Object.entries(model === "deal" ? $dealFields : $investorFields)
      .filter(([, v]) => v.isJson)
      .map(([k]) => k),
  )

  const isSubmodelKey = (key: string): key is SubmodelKey =>
    submodelKeys.includes(key as SubmodelKey)
  const isJsonKey = (key: string) => jsonKeys.includes(key)

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  let objDiff = $derived<Record<string, any>>(
    diff(oldObject.selected_version, $newObject.selected_version),
  )

  let oldDataSources = $derived(oldObject.selected_version.datasources)
  let newDataSources = $derived($newObject.selected_version.datasources)

  let oldQuotations = $derived(oldObject.selected_version.ds_quotations)
  let newQuotations: Quotations = $state({})

  $effect(() => {
    // create copy on mount
    newQuotations = $mutableObj.selected_version.ds_quotations
  })

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  let quotationsDiff = $derived<Record<string, any>>(
    diff(oldQuotations ?? {}, newQuotations),
  )

  let diffKeys: string[] = $derived(
    mergeKeys(objDiff, quotationsDiff).filter(k => k !== "ds_quotations"),
  )

  // let areAllChangesAttributed = $derived.by(() =>
  //   diffKeys.every(key => {
  //     const oldQuotes = oldQuotations[key] ?? []
  //     const newQuotes = newQuotations[key] ?? []
  //     const dsEqual =
  //       oldQuotes.length === newQuotes.length &&
  //       oldQuotes.every(q => newQuotes.map(q => q.nid).includes(q.nid))
  //     return newQuotes.length > 0 && !dsEqual
  //   }),
  // )

  // helpers to fix types
  const getValues = (key: string, object: object) => object.selected_version[key] ?? []

  const getQuotations = <T,>(key: string, quotations: Quotations) =>
    (quotations[key] ?? {}) as T

  $effect(() => {
    open = open
    clearSelected()
  })
</script>

<Modal bind:open class="h-3/4 w-3/4" dismissible>
  <div class="grid h-full grid-cols-4 grid-rows-[auto_1fr_auto] gap-2">
    <div class="col-span-full">
      <h2 class="heading4">{$_("Current changes")}</h2>
      <hr class="mb-2" />
    </div>

    <div class="col-span-3 overflow-y-scroll pr-3">
      <div class="col-span-3 flex flex-col gap-2">
        <div
          class="sticky top-0 flex gap-2 border-2 border-transparent bg-gray-50 p-2 dark:bg-gray-800"
        >
          <div class="flex basis-3/4 flex-col text-left">
            <b>{$_("Field")}</b>
            <div class="flex items-center gap-2">
              <del>{$_("OldValue")}</del>
              <span>&RightArrow;</span>
              <ins>{$_("NewValue")}</ins>
            </div>
          </div>

          <div class="flex basis-1/4 flex-col text-right">
            <div>
              <b>{$_("Sources updated?")}</b>
              <del><XIcon /></del>
              /
              <ins><CheckIcon /></ins>
            </div>
            <div class="flex items-center gap-2">
              <del>{$_("OldSources")}</del>
              <span>&RightArrow;</span>
              <ins>{$_("NewSources")}</ins>
            </div>
          </div>
        </div>

        {#each diffKeys as key}
          {#if isSubmodelKey(key)}
            <SubModelDiff
              {key}
              label={SUBMODEL_LABELS[key]}
              oldEntries={getValues(key, oldObject)}
              newEntries={getValues(key, $newObject)}
              oldQuotations={getQuotations<SubmodelQuotations>(key, oldQuotations)}
              newQuotations={getQuotations<SubmodelQuotations>(key, newQuotations)}
              {oldDataSources}
              {newDataSources}
            />
          {:else if isJsonKey(key)}
            {@const richField = getRichField(key)}

            <ChangedFieldItem onClick={() => {}} selectable={false}>
              <span>
                {$_('Preview for JSON field "{fieldname}" not yet available.', {
                  values: { fieldname: richField.label },
                })}
              </span>
            </ChangedFieldItem>
          {:else}
            {@const richField = getRichField(key)}
            {@const oldValue = getValues(key, oldObject)}
            {@const newValue = getValues(key, $newObject)}

            <ChangedFieldItem
              onClick={() => toggleSelected([key])}
              oldQuotes={getQuotations<FieldQuotations>(key, oldQuotations)}
              newQuotes={getQuotations<FieldQuotations>(key, newQuotations)}
              {oldDataSources}
              {newDataSources}
            >
              <span class="flex basis-3/4 flex-col text-left">
                {#if richField}
                  {@const DisplayField = richField.displayField}

                  {richField.label}

                  <div class="flex items-center gap-2">
                    {#if key in objDiff}
                      <del>
                        {#if oldValue && !(Array.isArray(oldValue) && oldValue.length === 0)}
                          <DisplayField value={oldValue} extras={richField.extras} />
                        {/if}
                      </del>
                      <span>&RightArrow;</span>
                      <ins>
                        {#if newValue && !(Array.isArray(newValue) && newValue.length === 0)}
                          <DisplayField value={newValue} extras={richField.extras} />
                        {/if}
                      </ins>
                    {:else}
                      <span class="italic">{$_("No value change")}</span>
                    {/if}
                  </div>
                {:else}
                  <span class="text-red">{$_("Unknown field")}: {key}</span>
                {/if}
              </span>
            </ChangedFieldItem>
          {/if}
        {/each}
      </div>
    </div>

    <aside class="overflow-y-scroll bg-gray-50 p-2 dark:bg-gray-800">
      <h4 class="heading5">{$_("Data Sources")}</h4>
      <DataSourceList dataSources={newDataSources} bind:quotations={newQuotations} />
    </aside>

    <div class="col-span-full flex gap-4">
      <!--      <span class="flex-grow">-->
      <!--        {#if areAllChangesAttributed}-->
      <!--          <ins><CheckIcon /></ins>-->
      <!--          {$_("All changes attributed")}-->
      <!--        {:else}-->
      <!--          <del><XIcon /></del>-->
      <!--          {$_("Not all changes attributed")}-->
      <!--        {/if}-->
      <!--      </span>-->
      <!-- svelte-ignore a11y_autofocus -->
      <button
        type="button"
        class="btn-outline"
        onclick={() => {
          open = false
        }}
        autofocus
      >
        {$_("Continue editing")}
      </button>
      <button
        type="button"
        class="btn btn-yellow"
        onclick={() => {
          $newObject.selected_version.ds_quotations = {
            ...oldQuotations,
            ...newQuotations,
          }
          onclick?.()
        }}
      >
        {$_("Save changes")}
      </button>
    </div>
  </div>
</Modal>

<style global lang="postcss">
  :global(del) {
    @apply text-red;
  }
  :global(ins) {
    @apply text-green no-underline;
  }
</style>
