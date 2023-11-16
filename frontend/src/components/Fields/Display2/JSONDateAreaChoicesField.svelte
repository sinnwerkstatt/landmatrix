<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { IntentionOfInvestment } from "$lib/types/deal"
  import type { JSONCurrentDateAreaChoicesFieldType } from "$lib/types/newtypes"

  import Label2 from "$components/Fields/Display2/Label2.svelte"
  import { dateCurrentFormat } from "$components/Fields/Display/jsonHelpers"
  import CircleNotchIcon from "$components/icons/CircleNotchIcon.svelte"

  export let value: JSONCurrentDateAreaChoicesFieldType = []

  export let fieldname: string
  export let label = ""
  export let hideLabel = false

  // $: flat_choices = formfield.choices
  //   ? Object.fromEntries(formfield.choices.map(c => [c.value, c.label]))
  //   : {}
</script>

<div class="mb-3 flex flex-wrap leading-5" data-fieldname={fieldname}>
  {#if !hideLabel}
    <Label2 value={label} class="md:w-5/12 lg:w-4/12" />
  {/if}
  <div class="text-lm-dark dark:text-white md:w-7/12 lg:w-8/12">
    <ul>
      {#each value ?? [] as val}
        <li class:font-bold={val.current}>
          <span>{dateCurrentFormat(val)}</span>
          {#if val.choices}
            CHOICES {val.choices}
            <!-- The literal translation strings are defined in apps/landmatrix/models/choices.py -->
            <!--{val.choices.map(v => $_(flat_choices[v])).join(", ")}-->
          {/if}
          {#if val.area}
            (
            <CircleNotchIcon />
            {val.area.toLocaleString("fr")}
            {$_("ha")})
          {/if}
        </li>
      {/each}
    </ul>
  </div>
</div>
