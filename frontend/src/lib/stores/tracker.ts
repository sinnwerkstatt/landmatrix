import { writable } from "svelte/store"

// https://developer.matomo.org/4.x/api-reference/tracking-javascript
export interface Tracker {
  disableCookies: () => void
  requireConsent: () => void
  setDoNotTrack: (bool: boolean) => void
  enableHeartBeatTimer: (activeTimeInSeconds: number) => void
  setCustomUrl: (url: string) => void
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  setCustomDimension: (dimensionID: number, value: any) => void
  trackPageView: (customTitle?: string) => void
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  trackEvent: (category: string, action: string, name?: string, value?: any) => void
}

export const tracker = writable<Tracker>()
