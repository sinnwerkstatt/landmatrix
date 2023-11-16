<script lang="ts">
  import Label2 from "$components/Fields/Display2/Label2.svelte"

  export let unit: string
  export let fieldname: string
  export let value: number | undefined
  export let label = ""
  export let hideLabel = false
</script>

<div class="mb-3 flex flex-wrap leading-5" data-fieldname={fieldname}>
  {#if !hideLabel}
    <Label2 value={label} class="md:w-5/12 lg:w-4/12 " />
  {/if}
  <div class="text-lm-dark dark:text-white md:w-7/12 lg:w-8/12">
    <div class="flex items-center">
      {value?.toLocaleString("fr") ?? "—"}
      {#if value && unit}
        {unit}
      {/if}
    </div>
  </div>
</div>
