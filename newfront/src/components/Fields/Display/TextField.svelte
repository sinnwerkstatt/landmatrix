<script lang="ts">
  import type { FormField } from "$components/Fields/fields"

  export let value: string
  export let formfield: FormField
</script>

<div class="text_field" data-name={formfield ? formfield.name : ""}>
  {#if !value}
    —
  {:else if formfield.class === "URLField"}
    <a href={value} target="_blank">{new URL(value).hostname}</a>
  {:else}
    {value}
  {/if}
</div>
