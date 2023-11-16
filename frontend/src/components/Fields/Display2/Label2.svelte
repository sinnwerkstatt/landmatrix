<script lang="ts">
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import { clickOutside } from "$lib/helpers"
  import { fieldDefinitions } from "$lib/stores"
  import type { FieldDefinition } from "$lib/types/generics"

  import type { FormField } from "$components/Fields/fields"
  import QuestionMarkCircleIcon from "$components/icons/QuestionMarkCircleIcon.svelte"

  export let value: string

  let showDefinition = false
</script>

<div
  class="flex items-center gap-2  font-medium {$$props.class ?? ''}"
  on:outClick={() => (showDefinition = false)}
  use:clickOutside
>
  {value}
  <!--{#if fd && $page.data.user.is_superuser}-->
  <!--  <div class="relative flex items-center">-->
  <!--    <button on:click|preventDefault={() => (showDefinition = true)}>-->
  <!--      <QuestionMarkCircleIcon class="h-5 w-5 text-lm-orange-400" />-->
  <!--    </button>-->
  <!--    {#if showDefinition}-->
  <!--      <div-->
  <!--        class="absolute top-full left-full z-30 w-80 border border-lm-black bg-gray-light px-4 py-3"-->
  <!--      >-->
  <!--        <div class="text-lg text-lm-purple-500">{value}</div>-->
  <!--        &lt;!&ndash;{fd.short_description}&ndash;&gt;-->
  <!--        &lt;!&ndash;{JSON.stringify(fd)}&ndash;&gt;-->
  <!--        &lt;!&ndash;x&ndash;&gt;-->
  <!--      </div>-->
  <!--    {/if}-->
  <!--  </div>-->
  <!--{/if}-->
</div>
