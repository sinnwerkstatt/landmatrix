<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { FormField } from "$components/Fields/fields"

  export let value: string
  export let formfield: FormField

  $: console.log(formfield.choices)
  $: flat_choices = formfield.choices
    ? Object.fromEntries(formfield.choices.map(c => [c.value, c.label]))
    : {}
</script>

<!-- The literal translation strings are defined in apps/landmatrix/models/choices.py -->
{value ? $_(flat_choices[value]) : "—"}
