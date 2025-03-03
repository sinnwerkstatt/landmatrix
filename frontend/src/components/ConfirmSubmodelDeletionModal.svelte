<script lang="ts">
  import { _ } from "svelte-i18n"

  import Modal from "$components/Modal.svelte"

  interface Props {
    open: boolean
    onconfirm: () => void
    onreject?: () => void
    submodelLabel: string
    id: string
    isDataSource?: boolean
  }

  let {
    open = $bindable(),
    onconfirm,
    onreject = () => (open = false),
    submodelLabel,
    id,
    isDataSource,
  }: Props = $props()
</script>

<Modal bind:open dismissible>
  <h2 class="heading4">
    {$_("Confirm deletion of {submodel}", { values: { submodel: submodelLabel } })}
  </h2>
  <hr />
  <div class="mb-12 mt-6 text-lg">
    {$_("Do you really want to delete {submodel}?", {
      values: { submodel: `${submodelLabel} #${id}` },
    })}
    <br />
    {#if isDataSource}
      <span class="text-red-500">{$_("WARNING")}</span>
      {$_("All all field references to this data source will be deleted as well.")}
    {/if}
  </div>
  <div class="flex justify-end gap-4">
    <!-- svelte-ignore a11y_autofocus -->
    <button type="button" class="btn-outline" onclick={onreject} autofocus>
      {$_("Reject")}
    </button>
    <button type="button" class="btn btn-yellow" onclick={onconfirm}>
      {$_("Confirm")}
    </button>
  </div>
</Modal>
