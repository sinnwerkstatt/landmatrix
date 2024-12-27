<script lang="ts">
  import { _ } from "svelte-i18n"

  interface Props {
    value: boolean | null
  }

  let { value }: Props = $props()
</script>

{#if value === true}
  {$_("Yes")}
{:else if value === false}
  {$_("No")}
{:else}
  —
{/if}
