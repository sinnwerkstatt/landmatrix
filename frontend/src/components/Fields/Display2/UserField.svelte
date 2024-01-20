<script lang="ts">
  import { allUsers } from "$lib/stores"

  export let value: number | null

  $: user = $allUsers.find(u => u.id === value)
</script>

{#if user}
  {user.full_name ?? user.username}
{:else}
  <!-- can't find this user anymore... -->
  <span class="italic">user #{value}</span>
{/if}
