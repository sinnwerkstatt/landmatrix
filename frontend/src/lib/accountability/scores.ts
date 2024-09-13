import { error } from "@sveltejs/kit"

import { goto } from "$app/navigation"
import { page } from "$app/stores"

import { getCsrfToken } from "$lib/utils"

export async function updateDealVariable(deal: number, variable: number, body: {}) {
  if (!deal || !variable)
    throw error(400, { message: "Deal ID and Variable must be defined" })
  try {
    const res = await fetch(`/api/accountability/deal/${deal}/${variable}/`, {
      method: "PATCH",
      credentials: "include",
      body: JSON.stringify(body),
      headers: {
        "X-CSRFToken": await getCsrfToken(),
        "Content-Type": "application/json",
      },
    })
    if (!res.ok) throw error(res.status, { message: res.statusText })
    return res
  } catch (error) {
    return error
  }
}
