<script lang="ts">
  import { _ } from "svelte-i18n";
  import type { FormField } from "../fields";

  export let formfield: FormField;
  export let value: Array<string | number> = [];

  $: value = value === null ? "" : value;
  //     set(v) {
  //         // deal with weird "[null]" array
  //         v = v.length === 1 && v[0] === null ? [] : v;
  //         this.$emit("input", v);
  //     },
</script>

<div class="simplearray_field">
  {#if formfield.choices}
    <div>
      <select bind:value multiple class="inpt">
        {#each Object.entries(formfield.choices) as [v, label]}
          <option value={v}>{label}</option>
        {/each}
      </select>
    </div>
  {:else}
    <div class="flex flex-col">
      <textarea
        value={value ? value.join("\n") : ""}
        on:input={(x) => (value = x.target.value.split("\n"))}
        class="inpt"
        rows="5"
      />
      <small class="form-text text-muted">
        {$_("Put each value on a new line, i.e. press enter between each name")}
      </small>
    </div>
  {/if}
</div>
