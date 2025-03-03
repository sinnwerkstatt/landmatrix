type _oneToNine = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
type _zeroToNine = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
type _YYYY = `19${_zeroToNine}${_zeroToNine}` | `20${_zeroToNine}${_zeroToNine}`
type _MM = `0${_oneToNine}` | `1${0 | 1 | 2}`
type _DD = `${0}${_oneToNine}` | `${1 | 2}${_zeroToNine}` | `3${0 | 1}`

export type LooseDateString = `${_YYYY}` | `${_YYYY}-${_MM}` | `${_YYYY}-${_MM}-${_DD}`
