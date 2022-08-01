<script lang="ts">
  import { gql } from "graphql-tag";
  import { _ } from "svelte-i18n";
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import { client } from "$lib/apolloClient";
  import { investorSections } from "$lib/sections";
  import type { DataSource } from "$lib/types/deal";
  import type { Investor } from "$lib/types/investor";
  import { removeEmptyEntries } from "$lib/utils/data_processing";
  import EditField from "$components/Fields/EditField.svelte";
  import LoadingSpinner from "$components/icons/LoadingSpinner.svelte";
  import SubmodelEditSection from "$components/Management/SubmodelEditSection.svelte";

  export let investor: Investor;
  export let investorID: number;
  export let investorVersion: number;

  let originalInvestor = JSON.stringify(investor);
  let savingInProgress = false;
  let showReallyQuitOverlay = false;
  $: activeTab = $page.url.hash || "#general";
  $: formChanged = JSON.stringify(investor) !== originalInvestor;
  $: tabs = [
    { target: "#general", name: $_("General info") },
    { target: "#parent_companies", name: $_("Parent companies") },
    { target: "#tertiary_investors", name: $_("Tertiary investors/lenders") },
    { target: "#data_sources", name: $_("Data sources") },
  ];

  async function saveInvestor(hash: string) {
    const currentForm = document.querySelector<HTMLFormElement>(activeTab);
    console.log(currentForm);
    if (!currentForm.checkValidity()) {
      currentForm.reportValidity();
      return;
    }
    savingInProgress = true;
    // investor.locations = removeEmptyEntries<Location>(investor.locations);
    // investor.contracts = removeEmptyEntries<Contract>(investor.contracts);
    investor.datasources = removeEmptyEntries<DataSource>(investor.datasources);

    const { data } = await $client.mutate({
      mutation: gql`
        mutation ($id: Int!, $version: Int, $payload: Payload) {
          investor_edit(id: $id, version: $version, payload: $payload) {
            investorId
            investorVersion
          }
        }
      `,
      variables: {
        id: investorID ? +investorID : -1,
        version: investorVersion ? +investorVersion : null,
        payload: { ...investor, versions: null, comments: null, workflowinfos: null },
      },
    });
    const { investor_edit } = data;
    originalInvestor = JSON.stringify(investor);
    savingInProgress = false;

    if (location.hash !== hash || +investorVersion !== +investor_edit.investorVersion) {
      await goto(
        `/investor/edit/${investor_edit.investorId}/${investor_edit.investorVersion}${
          hash ?? ""
        }`
      );
    }
  }

  const onClickClose = async (force: boolean) => {
    if (formChanged && !force) showReallyQuitOverlay = true;
    else if (!investorID) await goto("/");
    else
      await goto(
        `/investor/${investorID}${investorVersion ? "/" + investorVersion : ""}`
      );
  };
</script>

<div class="container mx-auto min-h-full h-full flex flex-col">
  <div class="md:flex md:flex-row md:justify-between border-b border-orange">
    <h1>
      {investorID ? $_("Editing Investor #") + investorID : $_("Adding new investor")}
    </h1>
    <div class="flex items-center my-5">
      <button
        type="submit"
        class="btn btn-primary mx-2 flex items-center gap-2"
        class:disabled={!formChanged || savingInProgress}
        on:click={() => saveInvestor(location.hash)}
      >
        {#if savingInProgress}
          <LoadingSpinner /> {$_("Saving...")}
        {:else}
          {$_("Save")}
        {/if}
      </button>
      {#if investorID}
        <button class="btn btn-secondary mx-2" on:click={() => onClickClose(false)}>
          {$_("Close")}
        </button>
      {:else}
        <button class="btn btn-gray btn-sm mx-2" on:click={() => goto(-1)}>
          {$_("Cancel")}
        </button>
      {/if}
    </div>
  </div>
  <div class="flex h-full overflow-y-hidden">
    <nav class="p-2 flex-initial">
      <ul>
        {#each tabs as { target, name }}
          <li
            class="py-2 pr-4 border-orange {activeTab === target
              ? 'border-r-4'
              : 'border-r'}"
          >
            {#if name}
              <a href={target} class:text-black={activeTab === target}>{name}</a>
            {:else}
              <hr />
            {/if}
          </li>
        {/each}
      </ul>
    </nav>
    <div class="pl-4 flex-auto w-full overflow-y-auto pr-2 pb-16">
      {#if activeTab === "#general"}
        <section>
          <form id="general">
            {#each investorSections.general_info as subsection}
              <div class="space-y-4 mt-2">
                <h3 class="my-0">{$_(subsection.name)}</h3>
                {#each subsection.fields as fieldname}
                  <EditField
                    model="investor"
                    {fieldname}
                    bind:value={investor[fieldname]}
                  />
                {/each}
              </div>
            {/each}
            <slot />
          </form>
        </section>
      {/if}
      {#if activeTab === "#parent_companies"}
        <SubmodelEditSection
          model="involvement"
          modelName="Parent company"
          bind:entries={investor.investors}
          entriesFilter={(i) => i.role === "PARENT"}
          newEntryExtras={{ role: "PARENT" }}
          id="parent_companies"
          fields={[
            "investor",
            "investment_type",
            "percentage",
            "loans_amount",
            "loans_currency",
            "loans_date",
            "parent_relation",
            "comment",
          ]}
        />
      {/if}
      {#if activeTab === "#tertiary_investors"}
        <SubmodelEditSection
          model="involvement"
          modelName="Tertiary investor/lender"
          bind:entries={investor.investors}
          entriesFilter={(i) => i.role === "LENDER"}
          newEntryExtras={{ role: "LENDER" }}
          id="tertiary_investors"
          fields={[
            "investor",
            "investment_type",
            "percentage",
            "loans_amount",
            "loans_currency",
            "loans_date",
            "comment",
          ]}
        />
      {/if}
      {#if activeTab === "#data_sources"}
        <SubmodelEditSection
          model="datasource"
          modelName="Data source"
          bind:entries={investor.datasources}
          id="data_sources"
        />
      {/if}
    </div>
  </div>
</div>
