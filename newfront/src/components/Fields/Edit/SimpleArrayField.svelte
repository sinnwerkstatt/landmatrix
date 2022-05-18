<script lang="ts">
  import { _ } from "svelte-i18n";
  import type { FormField } from "../fields";

  export let formfield: FormField;
  export let value: Array<string | number> = [];

  // computed: {
  //   val: {
  //     get() {
  //       let retval = this.value || [];
  //       if (!this.formfield.choices) {
  //         retval = retval.join("\n");
  //       }
  //       return retval;
  //     },
  //     set(v) {
  //       if (this.formfield.choices) {
  //         // deal with weird "[null]" array
  //         v = v.length === 1 && v[0] === null ? [] : v;
  //         this.$emit("input", v);
  //       } else {
  //         this.$emit("input", v.split("\n"));
  //       }
  //     },
  //   },
  // },
</script>

<div class="simplearray_field">
  {#if formfield.choices}
    <div>
      <select bind:value multiple class="inpt">
        {#each Object.entries(formfield.choices) as [value, label]}
          <option {value}>{label}</option>
        {/each}
      </select>
    </div>
  {:else}
    <!--this is not transformed yet -->
    <span class="italic text-red-600">HUHUHUHUHU!!!!</span>
    <div>
      <textarea v-model="val" class="form-control" />
      <small class="form-text text-muted">
        {$_("Put each value on a new line, i.e. press enter between each name")}
      </small>
    </div>
  {/if}
</div>
