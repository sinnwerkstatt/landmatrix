<script lang="ts">
  import dayjs from "dayjs"

  import type { FormField } from "$components/Fields/fields"

  export let formfield: FormField
  export let value: string
  export let format = "YYYY-MM-DD"

  // non-breaking hyphens would fix the stupid line break ("‑" vs "-")
  // return dayjs(this.value).format("YYYY‑MM‑DD"); 🤩️
</script>

<div class="date_field whitespace-nowrap" data-name={formfield ? formfield.name : ""}>
  {value ? dayjs(value).format(format) : "—"}
</div>
