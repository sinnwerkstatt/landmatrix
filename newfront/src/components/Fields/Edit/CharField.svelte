<script lang="ts">
  import { _ } from "svelte-i18n";
  import type { FormField } from "../fields";

  export let formfield: FormField;
  export let value: string;
</script>

<div class="char_field">
  <input
    bind:value
    type="text"
    class="inpt"
    placeholder={$_(formfield.label)}
    name={formfield.name}
    maxlength={formfield.max_length}
  />
</div>
