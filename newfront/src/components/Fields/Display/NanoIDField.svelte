<script lang="ts">
  import { page } from "$app/stores"

  import type { FormField } from "$components/Fields/fields"

  export let value: number
  export let formfield: FormField
</script>

<div class="nanoID_field" data-name={formfield ? formfield.name : ""}>
  <a class="font-mono" href="{$page.url.hash.split('/')[0] || '#locations'}/{value}">
    {value}
  </a>
</div>
