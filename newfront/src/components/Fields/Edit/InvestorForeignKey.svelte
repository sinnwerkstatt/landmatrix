<script lang="ts">
  import { gql } from "@apollo/client/core";
  import { _ } from "svelte-i18n";
  import Select from "svelte-select";
  import { client } from "$lib/apolloClient";
  import type { FormField } from "$components/Fields/fields";

  export let value: number;
  export let formfield: FormField;

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

<div class="investor_foreignkey_field">
  {#if investors}
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
      inputAttributes={{
        name: formfield.name,
      }}
    />
  {/if}
  {#if value}
    <div class="container p-2">
      <a href={`../../investor/${value.id}`} class="">
        Show details for investor #{value.id} {value.name}</a
      >
    </div>
  {/if}
  {#if investors.includes(value) === false}
    <!--    <div>Investor does not exist</div>-->
  {/if}
</div>
