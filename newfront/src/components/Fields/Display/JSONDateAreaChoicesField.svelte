<script lang="ts">
  import { _ } from "svelte-i18n";
  import type { IntentionOfInvestment } from "$lib/types/deal";
  import {
    dateCurrentFormat,
    mapChoices,
  } from "$components/Fields/Display/jsonHelpers";
  import type { FormField } from "$components/Fields/fields";
  import CircleNotchIcon from "$components/icons/CircleNotchIcon.svelte";

  type JSONDateAreaChoicesFieldType = {
    current?: boolean;
    name: string;
    area?: string;
    choices: Array<IntentionOfInvestment>;
  };

  export let formfield: FormField;
  export let value: JSONDateAreaChoicesFieldType[] = [];
</script>

<div class="jsondateareachoices_field">
  {#each value as val}
    <div class:font-bold={val.current}>
      <span>{dateCurrentFormat(val)} </span>
      {#if val.choices}
        {mapChoices(val.choices, formfield.choices)}
      {/if}
      {#if val.area}
        (<CircleNotchIcon /> {val.area.toLocaleString("fr")} {$_("ha")})
      {/if}
    </div>
  {/each}
</div>
