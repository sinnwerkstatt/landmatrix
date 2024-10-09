import { get } from "svelte/store"

import { tableSelection } from "./stores"

export function arrayIncludesAnyOf(array, values) {
  if (array instanceof Array && values instanceof Array) {
    return values.some(v => array.includes(v))
  } else {
    throw new Error("Both arguments must be arrays")
  }
}

export function arrayIncludesAllOf(array, values) {
  if (array instanceof Array && values instanceof Array) {
    return values.every(v => array.includes(v))
  } else {
    throw new Error("Both arguments must be arrays")
  }
}

export function groupBy(array: [], key: string, value: string) {
  const reduced = array.reduce((result, currentValue) => {
    if (!result[currentValue[key]]) {
      result[currentValue[key]] = []
    }
    value
      ? result[currentValue[key]].push(currentValue[value])
      : result[currentValue[key]].push(currentValue)
    return result
  }, {})
  let res = []
  Object.entries(reduced).forEach(([key, values]) => {
    res.push({ label: key, values })
  })
  return res
}

export function capitalizeFirst(string) {
  if (typeof string === "string") {
    const firstLetter = string.charAt(0)
    const firstLetterCap = firstLetter.toUpperCase()
    const remainingLetters = string.slice(1)
    const result = firstLetterCap + remainingLetters
    return result
  } else {
    throw new Error("Argument must be of type string")
  }
}

export function getStatusColor(status: string) {
  if (status == "TO_SCORE") return "bg-a-gray-200"
  if (status == "WAITING") return "bg-a-primary-500"
  if (status == "VALIDATED") return "bg-a-success-500"
  if (status == "NO_DATA") return "bg-a-gray-900"
  return ""
}

export function usersToUserChoices(users: {
  id: number
  name: string
  initials: string
}) {
  const result = users.map(({ id: value, name: label, initials }) => ({
    label,
    value: String(value),
    initials,
  }))
  return result
}

export function initTableSelection(deal) {
  const totalSelection = get(tableSelection)
  let dealSelection = totalSelection[deal.id]
  if (!dealSelection) totalSelection[deal.id] = { deal: deal.id, variables: {} }
  deal.score.variables.forEach(v => {
    if (!totalSelection[deal.id].variables[v.vggt_variable])
      totalSelection[deal.id].variables[v.vggt_variable] = false
  })

  // console.log(totalSelection)
  tableSelection.set(totalSelection)
}

export function sentenceToArray(string: string) {
  if (string) return string.match(/\b(\w+)\b/g)
  return [""]
}

export function searchMatch(string: string, filter: string) {
  return string.toLowerCase().indexOf(filter.toLocaleLowerCase()) >= 0
}

export function unique(myArray: []) {
  let newArray = myArray.filter((v, i, self) => {
    return i == self.indexOf(v)
  })
  return newArray
}
