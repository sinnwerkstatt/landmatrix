<script lang="ts">
  import { page } from "$app/stores"

  export let value: string
</script>

<a class="font-mono" href="{$page.url.hash.split('/')[0] || '#locations'}/{value}">
  {value}
</a>
