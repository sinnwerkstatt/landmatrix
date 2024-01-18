<script lang="ts">
  import { allUsers } from "$lib/stores"

  import { LABEL_CLASS, VALUE_CLASS, WRAPPER_CLASS } from "$components/Fields/consts"
  import Label2 from "$components/Fields/Display2/Label2.svelte"

  export let value: number | null
  export let fieldname: string
  export let label = ""
  export let wrapperClass = WRAPPER_CLASS
  export let labelClass = LABEL_CLASS
  export let valueClass = VALUE_CLASS

  $: user = $allUsers.find(u => u.id === value)
</script>

{#if value}
  <div class={wrapperClass} data-fieldname={fieldname}>
    {#if label}
      <Label2 value={label} class={labelClass} />
    {/if}
    <div class={valueClass}>
      {#if user}
        {user.full_name ?? user.username}
      {:else}
        <!-- can't find this user anymore... -->
        <span class="italic">{value}</span>
      {/if}
    </div>
  </div>
{/if}
