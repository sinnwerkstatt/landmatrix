<script lang="ts">
  import { _ } from "svelte-i18n"

  interface Props {
    value: string
    extras?: {
      url?: boolean
      ocid?: boolean
      email?: boolean
      investorNameUnknown?: boolean
    }
  }

  let {
    value,
    extras = {
      url: false,
      ocid: false,
      email: false,
      investorNameUnknown: false,
    },
  }: Props = $props()

  const safeGetHostname = (value: string): string => {
    try {
      return new URL(value).hostname
    } catch {
      return value
    }
  }
</script>

{#if extras.url}
  <a href={value} target="_blank" rel="noreferrer" class="break-all">
    {safeGetHostname(value)}
  </a>
  <!--{:else if extras.email}-->
  <!--  <a href="mailto://{value}">{value}</a>-->
{:else if extras.ocid}
  <a
    href="https://www.openlandcontracts.org/contract/{value}/view#/pdf"
    target="_blank"
    rel="noreferrer"
  >
    {$_("Access more information about this contract on OpenLandContracts.org")}
  </a>
{:else if extras.investorNameUnknown}
  <span class="italic text-gray-600">[{$_("unknown investor")}]</span>
{:else}
  <div style="word-break: break-word;" class="whitespace-pre-wrap">
    {value ?? "—"}
  </div>
{/if}
