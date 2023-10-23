<script lang="ts">
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import { fieldDefinitions } from "$lib/stores"
  import { clickOutside } from "$lib/helpers"
  import type { FieldDefinition } from "$lib/types/generics"

  import type { FormField } from "$components/Fields/fields"
  import QuestionMarkCircleIcon from "$components/icons/QuestionMarkCircleIcon.svelte"

  export let formfield: FormField
  export let model:
    | "deal"
    | "location"
    | "contract"
    | "datasource"
    | "investor"
    | "involvement" = "deal"

  let fd: FieldDefinition | undefined
  $: fd = $fieldDefinitions.find(
    fd => fd.model === model && fd.field === `${formfield?.name}`,
  )

  let showDefinition = false
</script>

<div
  class="flex items-center gap-2 {$$props.class ?? ''}"
  on:outClick={() => (showDefinition = false)}
  use:clickOutside
>
  {$_(formfield.label)}
  {#if fd && $page.data.user.is_superuser}
    <div class="relative flex items-center">
      <button on:click|preventDefault={() => (showDefinition = true)}>
        <QuestionMarkCircleIcon class="h-5 w-5 text-lm-orange-400" />
      </button>
      {#if showDefinition}
        <div
          class="absolute top-full left-full z-30 w-80 border border-lm-black bg-gray-light px-4 py-3"
        >
          <div class="text-lg text-lm-purple-500">{$_(formfield.label)}</div>
          {fd.short_description}
          <!--{JSON.stringify(fd)}-->
          <!--x-->
        </div>
      {/if}
    </div>
  {/if}
</div>
