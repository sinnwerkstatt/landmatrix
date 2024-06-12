<script lang="ts">
  import AtIcon from "$components/icons/AtIcon.svelte"
  import LinkIcon from "$components/icons/LinkIcon.svelte"

  export let value: string | string[]
  export let fieldname: string
  export let label = ""

  interface Extras {
    url?: boolean
    ocid?: boolean
    email?: boolean
    multiline?: boolean
    required?: boolean
  }

  export let extras: Extras = {
    url: false,
    ocid: false,
    email: false,
    multiline: false,
    required: false,
  }
</script>

{#if extras.multiline}
  <textarea bind:value class="inpt" name={fieldname} rows="5" placeholder={label} />
{:else if extras.url}
  <div class="flex">
    <input
      type="url"
      bind:value
      class="inpt"
      name={fieldname}
      required={extras.required}
      placeholder={label}
    />
    <div
      class="flex items-center justify-center border border-l-0 border-gray-300 bg-gray-200 px-3 py-1.5 text-gray-600"
    >
      <LinkIcon />
    </div>
  </div>
{:else if extras.email}
  <div class="flex">
    <input
      type="email"
      bind:value
      class="inpt"
      name={fieldname}
      required={extras.required}
      placeholder={label}
    />
    <div
      class="flex items-center justify-center border border-l-0 border-gray-300 bg-gray-200 px-3 py-1.5 text-gray-600"
    >
      <AtIcon />
    </div>
  </div>
{:else}
  <input
    type="text"
    bind:value
    class="inpt"
    name={fieldname}
    required={extras.required}
    placeholder={label}
  />
{/if}
