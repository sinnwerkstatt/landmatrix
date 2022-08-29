<script lang="ts">
  import dayjs from "dayjs";

  export let value: string;
  export let format = "YYYY-MM-DD";

  // non-breaking hyphens would fix the stupid line break ("‑" vs "-")
  // return dayjs(this.value).format("YYYY‑MM‑DD"); 🤩️
</script>

<div class="date_field whitespace-nowrap">
  {value ? dayjs(value).format(format) : "—"}
</div>
