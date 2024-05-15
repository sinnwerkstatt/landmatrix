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
