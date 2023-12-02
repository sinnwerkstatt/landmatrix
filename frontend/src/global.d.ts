// global.d.ts (or any ambient dts file)

import type { Tracker } from "$lib/stores/tracker"

declare global {
  interface Window {
    // Matomo
    Matomo?: {
      getTracker: (trackerUrl: string, siteId: number) => Tracker | undefined
    }

    // HCaptcha
    hcaptcha: HCaptcha
    hcaptchaOnLoad: (() => void) | null
  }
}

export {}
