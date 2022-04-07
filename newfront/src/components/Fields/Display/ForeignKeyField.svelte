<script lang="ts">
  import type { FormField } from "$components/Fields/fields";
  import { countries } from "$lib/stores";

  type ForeignKey = {
    id: number;
    name?: string;
    username?: string;
  };
  export let formfield: FormField;
  export let value: ForeignKey;
  export let model: string;
</script>

<div class="foreignkey_field">
  {#if !value || !value.id}
    <!-- no output -->
  {:else if formfield.related_model === "Investor"}
    <a class="investor" target="_blank" href="/investor/{value.id}">
      {value.name} (#{value.id})
    </a>
  {:else if formfield.related_model === "Country"}
    {$countries.find((c) => c.id === value.id).name}
  {:else}
    {value.username ?? value.name ?? value.id}
  {/if}
</div>
