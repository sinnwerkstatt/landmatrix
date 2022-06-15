<script lang="ts">
  import { gql } from "@apollo/client/core";
  import { _ } from "svelte-i18n";
  import Select from "svelte-select";
  import { client } from "$lib/apolloClient";

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
</div>
