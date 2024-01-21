<script lang="ts">
  import LinkIcon from "$components/icons/LinkIcon.svelte"

  export let value: string | string[]
  export let fieldname: string
  export let label = ""
  export let extras = { url: false, ocid: false, email: false, multiline: false }
</script>

{#if extras.multiline}
  <textarea bind:value class="inpt" name={fieldname} rows="5" placeholder={label} />
{:else if extras.url}
  <div class="flex">
    <input type="url" bind:value class="inpt" name={fieldname} placeholder={label} />
    <div
      class="flex items-center justify-center border border-l-0 border-gray-300 bg-gray-200 px-3 py-1.5 text-gray-600"
    >
      <LinkIcon class="h-4 w-4" />
    </div>
  </div>
{:else}
  <input type="text" bind:value class="inpt" name={fieldname} placeholder={label} />
{/if}
