<script lang="ts">
  import { _ } from "svelte-i18n";
  import type { Investor } from "$lib/types/investor";
  import DisplayField from "$components/Fields/DisplayField.svelte";
  import Overlay from "$components/Overlay.svelte";

  export let visible: boolean;
  export let investor: Investor;

  const fields = ["classification", "country", "homepage", "comment"];
  // const involvementFields = [
  //   "role",
  //   "investment_type",
  //   "percentage",
  //   "loans_amount",
  //   "loans_currency",
  //   "loans_date",
  //   "parent_relation",
  //   "comment",
  // ];
  const createTitle = (investor) => `${investor.name} (${investor.id})`;
</script>

<Overlay {visible} on:close title={createTitle(investor)}>
  <div>
    {#each fields as fieldName}
      <DisplayField
        fieldname={fieldName}
        value={investor[fieldName]}
        model="investor"
        showLabel
      />
    {/each}
    <!--{#if investor.involvements}-->
    <!--  {#each involvementFields as fieldName}-->
    <!--    <DisplayField-->
    <!--      fieldname={fieldName}-->
    <!--      value={investor.involvement[fieldName]}-->
    <!--      model="involvement"-->
    <!--      showLabel-->
    <!--    />-->
    <!--  {/each}-->
    <!--{/if}-->
    <div class="w-100">
      <a class="investor" target="_blank" href="/investor/{investor.id}">
        {$_("More details about this investor")}
      </a>
    </div>
  </div>
</Overlay>
