<script lang="ts">
  import { page } from "$app/state"
</script>

<div class="container mx-auto">
  <h1 class=" heading4 mt-10">
    {page.status}: {page.error.message}
  </h1>
</div>
