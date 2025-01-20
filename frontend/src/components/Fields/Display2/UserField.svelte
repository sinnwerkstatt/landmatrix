<script lang="ts">
  import { allUsers } from "$lib/stores"

  interface Props {
    value: number | null
  }

  let { value }: Props = $props()

  let user = $derived($allUsers.find(u => u.id === value))
</script>

{#if user}
  {user.full_name ?? user.username}
{:else}
  <!-- can't find this user anymore... -->
  <span class="italic">user #{value}</span>
{/if}
