<script lang="ts">
  import { _ } from "svelte-i18n";
  import type { FormField } from "../fields";

  export let formfield: FormField;
  export let value: number;
</script>

<div class="boolean_field">
  {#if formfield.class === "NullBooleanField"}
    <select bind:value class="inpt">
      {#if !formfield.required}<option value={null}>--------</option>{/if}
      <option value={true}>{$_("Yes")}</option>
      <option value={false}>{$_("No")}</option>
    </select>
  {:else}
    <input bind:checked={value} type="checkbox" class="inpt" />
  {/if}
</div>
