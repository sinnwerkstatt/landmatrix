<script lang="ts">
  import { page } from "$app/stores"
</script>

<div class="container mx-auto">
  <h1 class="mt-10">
    {$page.status}: {$page.error.message}
  </h1>
</div>
