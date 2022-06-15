<script lang="ts">
  import Select from "svelte-select";
  import type { FormField } from "../fields";

  export let formfield: FormField;
  export let value: string;
  export let required: boolean;

  let valueCopy = JSON.parse(JSON.stringify(value ?? []));

  $: value = formatValue(valueCopy);

  const formatValue = (valueCopy) => {
    const mapped = (valueCopy ?? []).map((item) => item.value);
    return mapped.length > 0 ? mapped : null;
  };
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
    hasError={required && !value}
  />
</div>
