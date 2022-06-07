<script lang="ts">
  import { _ } from "svelte-i18n";
  import type { FormField } from "../fields";

  export let formfield: FormField;
  export let value: string;
</script>

<div class="text_field">
  <textarea
    bind:value
    placeholder={$_(formfield.label)}
    name={formfield.name}
    rows="3"
    class="inpt"
  />
</div>
