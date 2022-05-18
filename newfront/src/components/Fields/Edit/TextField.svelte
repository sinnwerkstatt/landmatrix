<script lang="ts">
  import type { FormField } from "../fields";

  export let formfield: FormField;
  export let value: string;
</script>

<div class="text_field">
  {#if formfield.class === "TextField"}
    <textarea
      bind:value
      placeholder={formfield.label}
      name={formfield.name}
      rows="5"
      class="inpt"
    />
  {:else if formfield.class === "URLField"}
    <input
      bind:value
      type="url"
      placeholder={formfield.label}
      name={formfield.name}
      maxlength={formfield.max_length}
    />
  {:else}
    <input
      bind:value
      type="text"
      placeholder={formfield.label}
      name={formfield.name}
      maxlength={formfield.max_length}
    />
  {/if}
</div>
