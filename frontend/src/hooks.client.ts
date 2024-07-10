import * as Sentry from "@sentry/sveltekit"
import { handleErrorWithSentry } from "@sentry/sveltekit"
import { env } from "$env/dynamic/public"

Sentry.init({
  dsn: env.PUBLIC_SENTRY_DSN,
  environment: "svelte frontend",
  tracesSampleRate: 1.0,
  // For instance, initialize Session Replay:
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
  integrations: [Sentry.replayIntegration()],
})

// const myErrorHandler: HandleClientError = ({ error, event }) => {
//   console.error("An error occurred on the client side:", error, event)
// }

export const handleError = handleErrorWithSentry()
