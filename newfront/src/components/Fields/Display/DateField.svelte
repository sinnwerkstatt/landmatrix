<script lang="ts">
  import dayjs from "dayjs";
  import type { FormField } from "$components/Fields/fields";
  import DateField from "$components/Fields/Display/DateField.svelte";
  import { date } from "svelte-i18n";

  export let name: DateField;
  export let formfield: FormField;
  export let value: date | string;
  export let model: string;

  $: val = () => {
    if (value) {
      // non-breaking hyphens would fix the stupid line break ("‑" vs "-")
      // return dayjs(this.value).format("YYYY‑MM‑DD"); 🤩️
      if (value.length === 4) return value;
      if (value.length === 7) return value;
      return dayjs(value).format("YYYY-MM-DD");
    } else {
      return "n/a";
    }
  };
</script>

<div class="date_field whitespace-nowrap">{val()}</div>
