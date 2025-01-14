import ResizeObserver from "resize-observer-polyfill"

// @ts-expect-error global not defined
global.ResizeObserver = ResizeObserver
