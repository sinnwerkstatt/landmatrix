<script lang="ts">
  import Select from "svelte-select";
  import type { FormField } from "../fields";

  export let formfield: FormField;
  export let value: string;
  let array = [];
  array.push(formfield.choices);
  array.map((element) => {});
</script>

<div class="typed_choice_field">
  <Select
    bind:value
    class="inpt"
    items={formfield}
    name={formfield.name}
    isMulti={true}
  />
</div>
