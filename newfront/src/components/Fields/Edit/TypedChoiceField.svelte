<script lang="ts">
  import type { FormField } from "../fields";

  export let formfield: FormField;
  export let value: string;
</script>

<div class="typed_choice_field">
  <select bind:value class="inpt">
    {#each Object.entries(formfield.choices) as [value, label]}
      <option {value}>{label}</option>
    {/each}
  </select>
</div>
