<script lang="ts">
  import dayjs from "dayjs"

  export let value: string

  export let extras = { format: "YYYY-MM-DD" }

  // non-breaking hyphens would fix the stupid line break ("‑" vs "-")
  // return dayjs(this.value).format("YYYY‑MM‑DD"); 🤩️
</script>

{dayjs(value).format(extras.format)}

<!--{value ? dayjs(value).format(format) : "—"}-->
