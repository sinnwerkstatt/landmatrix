let selectedPaths: string[][] = $state([])

// todo maybe: use shorthand names and use as import * as selectedPaths from 'selectedPaths.svelte'
// public methods
export const getSelectedPaths = () => selectedPaths

export const anySelected = () => selectedPaths.length > 0

export const toggleSelected = (path: string[]) => {
  selectedPaths = toggle(path, selectedPaths)
}
export const clearSelected = () => {
  selectedPaths = []
}
// export const isSelected = (path: string[]) => includes(path, selectedPaths)

// pure helpers
const equal = (path1: string[], path2: string[]) =>
  path1.length === path2.length && path1.every((key, index) => key === path2[index])

const includes = (path: string[], paths: string[][]) => paths.some(p => equal(p, path))

const without = (path: string[], paths: string[][]) =>
  paths.filter(p => !equal(p, path))

const append = (path: string[], paths: string[][]) => [...paths, path]

const toggle = (path: string[], paths: string[][]) =>
  includes(path, paths) ? without(path, paths) : append(path, paths)
