<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { FormField } from "$components/Fields/fields"

  enum ActorRole {
    TRADITIONAL_LAND_OWNERS_OR_COMMUNITIES = "TRADITIONAL_LAND_OWNERS_OR_COMMUNITIES",
    GOVERNMENT_OR_STATE_INSTITUTIONS = "GOVERNMENT_OR_STATE_INSTITUTIONS",
    TRADITIONAL_LOCAL_AUTHORITY = "TRADITIONAL_LOCAL_AUTHORITY",
    BROKER = "BROKER",
    INTERMEDIARY = "INTERMEDIARY",
    OTHER = "OTHER",
  }

  type JSONActorsFieldType = {
    name: string
    role: ActorRole
  }

  export let formfield: FormField
  export let value: JSONActorsFieldType[] = []
</script>

<ul class="jsonactors_field list-disc pl-5" data-name={formfield?.name ?? ""}>
  {#each value ?? [] as val}
    <li>
      <span>{val.name}</span>
      {#if val.role}
        <span class="text-sm font-light">
          <!-- The literal translation strings are defined in apps/landmatrix/models/choices.py -->
          ({$_(formfield.choices[val.role])})
        </span>
      {/if}
    </li>
  {/each}
</ul>
