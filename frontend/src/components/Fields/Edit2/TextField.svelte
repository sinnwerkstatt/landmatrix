<script lang="ts">
  import { LABEL_CLASS, VALUE_CLASS, WRAPPER_CLASS } from "$components/Fields/consts"
  import Label2 from "$components/Fields/Display2/Label2.svelte"
  import LinkIcon from "$components/icons/LinkIcon.svelte"

  export let value: string | string[]
  export let fieldname: string
  export let label = ""
  export let wrapperClass = WRAPPER_CLASS
  export let labelClass = LABEL_CLASS
  export let valueClass = VALUE_CLASS

  export let multiline = false
  export let isURL = false
</script>

<div class={wrapperClass} data-fieldname={fieldname}>
  {#if label}
    <Label2 value={label} class={labelClass} />
  {/if}
  <div class={valueClass}>
    {#if multiline}
      <textarea bind:value class="inpt" name={fieldname} rows="5" placeholder={label} />
    {:else if isURL}
      <div class="flex">
        <input
          type="url"
          bind:value
          class="inpt"
          name={fieldname}
          placeholder={label}
        />
        <div
          class="flex items-center justify-center border border-l-0 border-gray-300 bg-gray-200 px-3 py-1.5 text-gray-600"
        >
          <LinkIcon class="h-4 w-4" />
        </div>
      </div>
    {:else}
      <input type="text" bind:value class="inpt" name={fieldname} placeholder={label} />
    {/if}
  </div>
</div>
