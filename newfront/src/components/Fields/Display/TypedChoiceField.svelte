<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { FormField } from "$components/Fields/fields"

  export let value: string
  export let formfield: FormField
</script>

<div
  class="typed_choice_field whitespace-nowrap"
  data-name={formfield ? formfield.name : ""}
>
  {value ? $_(formfield.choices[value]) : "—"}
</div>
