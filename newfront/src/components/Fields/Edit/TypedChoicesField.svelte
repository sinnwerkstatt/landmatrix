<script lang="ts">
  import Select from "svelte-select";
  import type { FormField } from "../fields";

  export let formfield: FormField;
  export let value: string;

  let valCopy = JSON.parse(JSON.stringify(value));

  $: value = (valCopy ?? []).map((item) => item.value);
</script>

<div class="typed_choice_field">
  <Select
    bind:value={valCopy}
    class="inpt"
    items={Object.entries(formfield.choices).map(([value, label]) => ({
      value,
      label,
    }))}
    name={formfield.name}
    isMulti={true}
  />
</div>
