<script module lang="ts">
  export const FILE_TYPES = ["csv", "xlsx", "json"] as const
  export type FileType = (typeof FILE_TYPES)[number]
  export type DownloadEvent = CustomEvent<FileType>
</script>

<script lang="ts">
  import { createEventDispatcher } from "svelte"
  import { _ } from "svelte-i18n"

  import Modal from "$components/Modal.svelte"

  const dispatch = createEventDispatcher<{ download: FileType }>()

  interface Props {
    open: boolean
    disableSubmit?: boolean
    fileTypes?: readonly FileType[]
  }

  let {
    open = $bindable(),
    disableSubmit = false,
    fileTypes = FILE_TYPES,
  }: Props = $props()

  let fileTypeGroup: FileType = $state(fileTypes[0])

  const download = () => {
    dispatch("download", fileTypeGroup)
  }
</script>

<Modal bind:open dismissible>
  <h4 class="heading4">
    {$_("Download")}
  </h4>
  <hr />
  <form class="mt-6 text-lg" onsubmit={download}>
    <div class="flex flex-col">
      {#each fileTypes as format}
        <div>
          <input
            id="download-{format}"
            type="radio"
            name="download-type"
            bind:group={fileTypeGroup}
            value={format}
          />
          <label for="download-{format}" class="uppercase">{format}</label>
        </div>
      {/each}
    </div>

    <div class="mt-14 flex justify-end gap-4">
      <button class="btn-outline" onclick={() => (open = false)} type="button">
        {$_("Cancel")}
      </button>
      <button class="btn btn-violet" type="submit" disabled={disableSubmit}>
        {$_("Download")}
      </button>
    </div>
  </form>
</Modal>
