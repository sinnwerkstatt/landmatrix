<script lang="ts" module>
  export interface SubModel {
    key: string
    label: string
  }
</script>

<script lang="ts">
  import { diff } from "deep-object-diff"
  import { _ } from "svelte-i18n"
  import type { Writable } from "svelte/store"

  import { dealFields, investorFields } from "$lib/fieldLookups"
  import { getTypedKeys } from "$lib/helpers"
  import type { Model } from "$lib/types/data"

  import SubModelDiff from "$components/DSQuotations/SubModelDiff.svelte"
  import CheckIcon from "$components/icons/CheckIcon.svelte"
  import XIcon from "$components/icons/XIcon.svelte"
  import Modal from "$components/Modal.svelte"

  interface Props {
    open: boolean
    model?: Model
    oldObject: object
    newObject: Writable<object>
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

  export const subModels: SubModel[] = [
    { key: "locations", label: $_("Locations") },
    { key: "contracts", label: $_("Contracts") },
    { key: "datasources", label: $_("Data Sources") },
    { key: "involvements", label: $_("Involvements") },
  ]

  let objDiff = $derived(diff(oldObject.selected_version, $newObject.selected_version))

  let oldDataSources = $derived(oldObject.selected_version.datasources)
  let oldQuotations = $derived(oldObject.selected_version.ds_quotations)

  let newDataSources = $derived($newObject.selected_version.datasources)
  let newQuotations: { [key: string]: { nid: string }[] | undefined } = $state({})

  $effect(() => {
    newQuotations = oldQuotations
  })

  let fieldKeys: string[] = $derived.by(() => {
    const subModelKeys = subModels.map(m => m.key)
    return getTypedKeys(objDiff).filter(
      k => !subModelKeys.includes(k) && k !== "ds_quotations",
    )
  })

  let selectedDiffKeys: string[] = $state([])

  let doOverwriteOldQuotations = $state(true)
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
            <b>Field Name</b>
            <div class="flex items-center gap-2">
              <del>OldValue</del>
              <span>&RightArrow;</span>
              <ins>NewValue</ins>
            </div>
          </div>

          <div class="flex basis-1/4 flex-col text-right">
            <div>
              <b>Sources updated?</b>
              <del><XIcon /></del>
              /
              <ins><CheckIcon /></ins>
            </div>
            <div class="flex items-center gap-2">
              <del>OldSources</del>
              <span>&RightArrow;</span>
              <ins>NewSources</ins>
            </div>
          </div>
        </div>

        {#each subModels as subModel}
          {#if subModel.key in objDiff}
            <SubModelDiff
              {subModel}
              original={oldObject.selected_version[subModel.key]}
              updated={$newObject.selected_version[subModel.key]}
            />
          {/if}
        {/each}

        {#each fieldKeys as key}
          {@const richField = getRichField(key)}
          {@const oldQuotes = oldQuotations[key] ?? []}
          {@const newQuotes = newQuotations[key] ?? []}
          {@const oldValue = oldObject.selected_version[key]}
          {@const newValue = $newObject.selected_version[key]}
          {@const dsEqual =
            oldQuotes.length === newQuotes.length &&
            oldQuotes.every(q => newQuotes.map(q => q.nid).includes(q.nid))}

          <button
            type="button"
            class="flex gap-2 border-2 p-2 {selectedDiffKeys.includes(key)
              ? 'border-yellow bg-yellow/20'
              : ''}"
            onclick={() =>
              (selectedDiffKeys = selectedDiffKeys.includes(key)
                ? selectedDiffKeys.filter(k => k !== key)
                : [...selectedDiffKeys, key])}
          >
            <span class="flex basis-3/4 flex-col text-left">
              {#if richField}
                {@const DisplayField = richField.displayField}

                {richField.label}

                <div class="flex items-center gap-2">
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
                </div>
              {:else}
                <span class="text-red">Unknown field {key}</span>
              {/if}
            </span>

            <span class="flex basis-1/4 flex-col text-right">
              {#if dsEqual}
                <del><XIcon /></del>
              {:else}
                <ins><CheckIcon /></ins>
              {/if}
              <div class="flex items-center justify-end gap-2">
                <div>
                  {oldQuotes.length > 0
                    ? oldQuotes
                        .map(q => oldDataSources.findIndex(ds => ds.nid === q.nid) + 1)
                        .join(", ")
                    : ""}
                </div>
                <span>&RightArrow;</span>
                <div>
                  {newQuotes.length > 0
                    ? newQuotes
                        .map(q => oldDataSources.findIndex(ds => ds.nid === q.nid) + 1)
                        .join(", ")
                    : ""}
                </div>
              </div>
            </span>
          </button>
        {/each}
      </div>
    </div>

    <aside class="overflow-y-scroll bg-gray-50 p-2 dark:bg-gray-800">
      <h4 class="heading5">{$_("Data Sources")}</h4>

      <!--{#if !selectedDiffKey}-->
      <!--  <CheckboxSwitch-->
      <!--    class="m-0 px-0 pb-2"-->
      <!--    id="replace-sources-switch"-->
      <!--    bind:checked={doOverwriteOldQuotations}-->
      <!--    onchange={() => showContextHelp.toggle()}-->
      <!--  >-->
      <!--    Replace sources-->
      <!--  </CheckboxSwitch>-->
      <!--{/if}-->

      <ol class="flex flex-col gap-2">
        {#each newDataSources as dataSource, i}
          <li>
            {#if selectedDiffKeys}
              {@const keysWithQuotation = selectedDiffKeys.filter(k =>
                (newQuotations[k] ?? []).map(q => q.nid).includes(dataSource.nid),
              )}
              {@const isAll =
                keysWithQuotation.length > 0 &&
                keysWithQuotation.length === selectedDiffKeys.length}
              {@const isAny =
                keysWithQuotation.length > 0 &&
                keysWithQuotation.length !== selectedDiffKeys.length}
              <button
                class="w-full p-2 text-left {isAll
                  ? 'bg-yellow'
                  : isAny
                    ? 'bg-yellow/20'
                    : 'bg-white dark:bg-gray-500'}"
                type="button"
                onclick={() => {
                  const _isAll = isAll
                  selectedDiffKeys.forEach(k => {
                    newQuotations[k] = (newQuotations[k] ?? []).filter(
                      q => q.nid !== dataSource.nid,
                    )
                  })
                  if (!_isAll) {
                    selectedDiffKeys.forEach(k => {
                      newQuotations[k] = [
                        ...(newQuotations[k] ?? []),
                        { nid: dataSource.nid },
                      ]
                    })
                  }
                }}
              >
                {i + 1}. {dataSource.nid}
              </button>
            {:else}
              {@const allHaveDataSource = fieldKeys.every(key => {
                const quotes = newQuotations[key] ?? []
                return (
                  quotes.length > 0 && quotes.map(q => q.nid).includes(dataSource.nid)
                )
              })}

              <button
                class="w-full p-2 text-left {allHaveDataSource
                  ? 'bg-yellow'
                  : 'bg-white dark:bg-gray-500'}"
                type="button"
                onclick={() => {
                  {
                    if (allHaveDataSource) {
                      newQuotations = Object.fromEntries(
                        Object.entries(newQuotations).map(([key, quotes]) => [
                          key,
                          quotes.filter(q => q.nid !== dataSource.nid),
                        ]),
                      )
                    } else {
                      const newQuote = { nid: dataSource.nid }
                      newQuotations = Object.fromEntries(
                        fieldKeys.map(key => {
                          return [
                            key,
                            doOverwriteOldQuotations
                              ? [newQuote]
                              : [...(newQuotations[key] ?? []), newQuote],
                          ]
                        }),
                      )
                    }
                  }
                }}
              >
                {i + 1}. {dataSource.nid}
              </button>
            {/if}
          </li>
        {/each}
      </ol>
    </aside>

    <div class="col-span-full flex justify-end gap-4">
      <!-- svelte-ignore a11y_autofocus -->
      <button
        type="button"
        class="btn-outline"
        onclick={() => (open = false)}
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

<style lang="postcss">
  del {
    @apply text-red;
  }
  ins {
    @apply text-green no-underline;
  }
</style>
