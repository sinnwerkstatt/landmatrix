import type { ComponentType } from "svelte"
import { _ } from "svelte-i18n"
import { derived } from "svelte/store"

import DecimalField from "$components/Fields/Display2/DecimalField.svelte"
import JSONCurrentDateAreaChoicesField from "$components/Fields/Display2/JSONCurrentDateAreaChoicesField.svelte"
import JSONCurrentDateAreaField from "$components/Fields/Display2/JSONCurrentDateAreaField.svelte"
import TextField from "$components/Fields/Display2/TextField.svelte"

interface Sec {
  displayField: ComponentType
  label: string
}

// export const investorSections = derived(_, $_ => {
//   return {
//     country: {
//       displayField: CountryField,
//       label: $_("Country of registration/origin"),
//     },
//   } as { [key: string]: Sec }
// })

export const dealFields = derived(_, $_ => {
  return {
    // Land area
    intended_size: {
      displayField: DecimalField,
      label: $_("Intended size"),
    },
    contract_size: {
      displayField: JSONCurrentDateAreaField,
      label: $_("Size under contract (leased or purchased area)"),
    },
    production_size: {
      displayField: JSONCurrentDateAreaField,
      label: $_("Size in operation (production)"),
    },
    land_area_comment: {
      displayField: TextField,
      label: $_("Comment on land area"),
    },
    //   Intention of investment
    intention_of_investment: {
      displayField: JSONCurrentDateAreaChoicesField,
      label: $_("Intention of investment"),
    },
    intention_of_investment_comment: {
      displayField: TextField,
      label: $_("Comment on intention of investment"),
    },
  } as { [key: string]: Sec }
})
