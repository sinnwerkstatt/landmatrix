<script lang="ts">
  import { gql } from "graphql-tag";
  import { onMount } from "svelte";
  import { _ } from "svelte-i18n";
  import Select from "svelte-select";
  import VirtualList from "svelte-tiny-virtual-list";
  import { page } from "$app/stores";
  import EditField from "$components/Fields/EditField.svelte";
  import type { FormField } from "$components/Fields/fields";

  export let value: Investor;
  export let formfield: FormField;

  type Investor = {
    id?: number;
    name: string;
  };

  let investors: Investor[] = [];
  async function getInvestors() {
    const { data } = await $page.stuff.secureApolloClient.query<{
      investors: Investor[];
    }>({
      query: gql`
        query {
          investors(
            sort: "name"
            limit: 0
            subset: UNFILTERED
            filters: [{ field: "status", value: 4, exclusion: true }]
          ) {
            id
            name
          }
        }
      `,
    });
    investors = [...data.investors];
  }

  onMount(() => {
    getInvestors();
  });

  let newInvestor: Investor = {} as Investor;
  let newInvestorForm: HTMLFormElement;
  let showNewInvestorForm = false;
  function initCreateNewInvestor({ detail }) {
    newInvestor = { name: detail };
    showNewInvestorForm = true;
  }
  function addNewInvestor() {
    if (!newInvestorForm.checkValidity()) {
      newInvestorForm.reportValidity();
      return;
    }
    return $page.stuff.secureApolloClient
      .mutate({
        mutation: gql`
          mutation ($payload: Payload) {
            investor_edit(id: -1, payload: $payload) {
              investorId
              investorVersion
            }
          }
        `,
        variables: { payload: newInvestor },
      })
      .then(({ data: { investor_edit } }) => {
        let newI = { id: investor_edit.investorId, name: newInvestor.name };
        investors.push(newI);
        // dispatch("input", newI);
        value = newI;
        newInvestor = {} as Investor;
        showNewInvestorForm = false;
      });
  }
</script>

<div class="investor_foreignkey_field">
  {#if investors}
    <Select
      items={investors}
      {value}
      on:select={({ detail }) => (value = { id: detail.id, name: detail.name })}
      on:clear={() => (value = null)}
      placeholder={$_("Investor")}
      optionIdentifier="id"
      labelIdentifier="name"
      getOptionLabel={(o, ftxt) =>
        o.isCreator ? `Create "${ftxt}"` : `${o.name} (#${o.id})`}
      getSelectionLabel={(o) => `${o.name} (#${o.id})`}
      showChevron
      isCreatable
      createItem={(ftxt) => ({ name: ftxt, id: "new" })}
      on:itemCreated={initCreateNewInvestor}
      inputAttributes={{ name: formfield.name }}
      {VirtualList}
    />
  {/if}
  {#if !showNewInvestorForm && value}
    <div class="container p-2">
      <a href="/investor/{value.id}" class="">
        {$_("Show details for investor")} #{value.id} {value.name}</a
      >
    </div>
  {/if}
  {#if showNewInvestorForm}
    <form bind:this={newInvestorForm} on:submit|preventDefault={addNewInvestor}>
      <div class="container">
        {#each ["name", "country", "classification", "homepage", "opencorporates", "comment"] as fieldname}
          <EditField
            {fieldname}
            bind:value={newInvestor[fieldname]}
            model="investor"
            wrapperClasses="flex justify-center items-center my-2"
            labelClasses="font-bold w-5/12"
            valueClasses="w-7/12 mb-1"
          />
        {/each}
      </div>
      <button type="submit" class="btn btn-primary">{$_("Save")}</button>
    </form>
  {/if}
</div>
