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
