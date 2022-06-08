<script lang="ts">
  import { _ } from "svelte-i18n";

  export let value: string;

  // non-breaking hyphens would fix the stupid line break ("‑" vs "-")
  // return dayjs(this.value).format("YYYY‑MM‑DD"); 🤩️
</script>

<div class="date_field whitespace-nowrap">{value ?? $_("n/a")}</div>
