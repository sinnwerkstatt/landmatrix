<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import { _ } from "svelte-i18n";
  import type { Investor } from "$lib/types/investor";
  import ManageOverlay from "$components/Management/ManageOverlay.svelte";
  import ManageHeader from "./ManageHeader.svelte";

  const dispatch = createEventDispatcher();

  export let investor: Investor;
  export let investorVersion: number;

  let showSendToReviewOverlay = false;
</script>

<ManageHeader object={investor} objectVersion={investorVersion} otype="investor">
  <div slot="heading">
    {investor.name} <small>#{investor.id}</small>
  </div>
</ManageHeader>

<ManageOverlay
  bind:visible={showSendToReviewOverlay}
  title={$_("Submit for review")}
  commentInput
  on:submit={() => console.log("change_status", { transition: "TO_REVIEW" })}
>
  <div class="mb-6">
    <label for="data-policy-checkbox" class="underline">{$_("Data policy")}</label>
    <label class="font-bold block mt-1">
      <input required type="checkbox" id="data-policy-checkbox" />
      {$_("I've read and agree to the")}
      <a href="/about/data-policy/" target="_blank">{$_("Data policy")} </a>.
    </label>
  </div>
</ManageOverlay>
