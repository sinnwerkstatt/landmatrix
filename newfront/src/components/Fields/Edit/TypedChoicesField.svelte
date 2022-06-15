<script lang="ts">
  import Select from "svelte-select";
  import type { FormField } from "../fields";

  export let formfield: FormField;
  export let value: string;

  let valueCopy = JSON.parse(JSON.stringify(value));

  $: value = (valueCopy ?? []).map((item) => item.value) ?? null;
</script>

<div class="typed_choices_field">
  <Select
    bind:value={valueCopy}
    class="inpt"
    items={Object.entries(formfield.choices).map(([value, label]) => ({
      value,
      label,
    }))}
    name={formfield.name}
    isMulti={true}
    required={true}
  />
</div>
