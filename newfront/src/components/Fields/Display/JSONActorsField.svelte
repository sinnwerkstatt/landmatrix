<script lang="ts">
  import { mapChoices } from "$components/Fields/Display/jsonHelpers";
  import type { FormField } from "$components/Fields/fields";

  enum ActorRole {
    TRADITIONAL_LAND_OWNERS_OR_COMMUNITIES = "TRADITIONAL_LAND_OWNERS_OR_COMMUNITIES",
    GOVERNMENT_OR_STATE_INSTITUTIONS = "GOVERNMENT_OR_STATE_INSTITUTIONS",
    TRADITIONAL_LOCAL_AUTHORITY = "TRADITIONAL_LOCAL_AUTHORITY",
    BROKER = "BROKER",
    INTERMEDIARY = "INTERMEDIARY",
    OTHER = "OTHER",
  }

  type JSONActorsFieldType = {
    name: string;
    role: ActorRole;
  };

  export let formfield: FormField;
  export let value: JSONActorsFieldType[] = [];
</script>

<div class="jsonactors_field whitespace-nowrap">
  {#each value as val}
    <div>
      <span>{val.name}</span>
      {#if val.role}
        <span class="font-weight-light">
          ({mapChoices(val.role, formfield.choices)})
        </span>
      {/if}
    </div>
  {/each}
</div>
