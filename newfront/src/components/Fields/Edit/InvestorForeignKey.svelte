<script lang="ts">
  import { gql } from "@apollo/client/core";
  import { _ } from "svelte-i18n";
  import Select from "svelte-select";
  import { client } from "$lib/apolloClient";
  import EditField from "../EditField.svelte";

  export let value: number;

  type Investor = {
    id: number;
    name: string;
  };

  let investors: Investor[] = [];
  async function getInvestors() {
    const { data } = await $client.query<{ investors: Investor[] }>({
      query: gql`
        query {
          investors {
            id
            name
          }
        }
      `,
    });
    investors = data.investors;
  }
  getInvestors();
</script>

<div class="currency_foreignkey_field">
  {#if investors}
    <!--{JSON.stringify(investors)}-->
    <!--{JSON.stringify(value)}-->
    <Select
      items={investors}
      {value}
      on:select={(x) => (value = { ...x.detail, code: undefined })}
      placeholder={$_("Investor")}
      optionIdentifier="id"
      labelIdentifier="name"
      getOptionLabel={(o) => `${o.name} (#${o.id})`}
      getSelectionLabel={(o) => `${o.name} (#${o.id})`}
      showChevron
    />
  {/if}
  {#if value}
    <div class="container p-2">
      <!--      <a href={`../../investor/${value.id}`} class=""-->
      <!--        ><button class="rounded bg-pelorous py-1 px-2 mr-1 text-white font-bold "-->
      <!--          >{value.id}</button-->
      <!--        >-->
      <!--        <span class="text-black">{value.name}</span></a-->
      <!--      >-->
      <a href={`../../investor/${value.id}`} class="">
        Show details for #{value.id} {value.name}...</a
      >
    </div>
  {/if}
</div>
