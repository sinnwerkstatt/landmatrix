// global.d.ts (or any ambient dts file)

declare global {
  interface Window {
    // HCaptcha
    hcaptcha: HCaptcha
    hcaptchaOnLoad: (() => void) | null
  }
}

export {}
