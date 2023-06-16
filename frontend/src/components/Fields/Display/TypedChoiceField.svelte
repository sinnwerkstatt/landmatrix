<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { FormField } from "$components/Fields/fields"

  export let value: string
  export let formfield: FormField
</script>

<!-- The literal translation strings are defined in apps/landmatrix/models/choices.py -->
{value ? $_(formfield.choices[value]) : "—"}
