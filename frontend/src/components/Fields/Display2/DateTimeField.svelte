<script lang="ts">
  import dayjs from "dayjs"

  interface Props {
    value: string
    extras?: { format: string }
  }

  let { value, extras = { format: "YYYY-MM-DD" } }: Props = $props()

  // non-breaking hyphens would fix the stupid line break ("‑" vs "-")
  // return dayjs(this.value).format("YYYY‑MM‑DD"); 🤩️
</script>

{dayjs(value).format(extras.format)}

<!--{value ? dayjs(value).format(format) : "—"}-->
