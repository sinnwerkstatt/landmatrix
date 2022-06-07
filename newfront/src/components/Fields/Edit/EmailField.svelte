<script lang="ts">
  import { _ } from "svelte-i18n";
  import AtIcon from "$components/icons/AtIcon.svelte";
  import type { FormField } from "../fields";

  export let formfield: FormField;
  export let value: string;
</script>

<div class="email_field flex">
  <input
    bind:value
    type="email"
    class="inpt"
    placeholder={$_(formfield.label)}
    maxlength={formfield.max_length}
  />
  <div
    class="flex justify-center items-center border border-l-0 border-gray-300 py-1.5 px-3 bg-gray-200 text-gray-600"
  >
    <AtIcon class="h-4 w-4" />
  </div>
</div>
