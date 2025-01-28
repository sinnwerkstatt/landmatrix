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

  let fieldKeys: string[] = $derived.by(() => {
    const subModelKeys = subModels.map(m => m.key)
    return getTypedKeys(objDiff).filter(k => !subModelKeys.includes(k))
  })
</script>

<Modal bind:open class="w-2/3" dismissible>
  <h2 class="heading4">{$_("Current changes")}</h2>
  <hr />

  <h3 class="heading5 mt-2">{$_("Submodels")}</h3>

  <div class="flex flex-col gap-2">
    {#each subModels as subModel}
      {#if subModel.key in objDiff}
        <SubModelDiff
          {subModel}
          original={oldObject.selected_version[subModel.key]}
          updated={$newObject.selected_version[subModel.key]}
        />
      {/if}
    {/each}
  </div>

  <h3 class="heading5 mt-2">{$_("Fields")}</h3>

  <div class="flex flex-col gap-2">
    {#each fieldKeys as key}
      {@const richField = getRichField(key)}
      {@const oldValue = oldObject.selected_version[key]}
      {@const newValue = $newObject.selected_version[key]}

      <div>
        {richField.label}
        <span class="text-red">
          {oldValue}
        </span>
        <span class="text-green">
          {newValue}
        </span>
      </div>
    {/each}
  </div>

  <div class="mt-2 flex justify-end gap-4">
    <!-- svelte-ignore a11y_autofocus -->
    <button type="button" class="btn-outline" onclick={() => (open = false)} autofocus>
      {$_("Continue editing")}
    </button>
    <button type="button" class="btn btn-yellow" {onclick}>
      {$_("Save changes")}
    </button>
  </div>
</Modal>
