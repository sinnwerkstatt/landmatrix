<script lang="ts">
  import dayjs from "dayjs";
  import type { FormField } from "$components/Fields/fields";

  export let formfield: FormField;
  export let value: string;
  export let model: string;

  // non-breaking hyphens would fix the stupid line break ("‑" vs "-")
  // return dayjs(this.value).format("YYYY‑MM‑DD"); 🤩️
  $: val = value
    ? value.length === 4 || value.length === 7
      ? value
      : dayjs(value).format("YYYY-MM-DD")
    : "n/a";
</script>

<div class="date_field whitespace-nowrap">{val}</div>
