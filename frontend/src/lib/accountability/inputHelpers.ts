// Helper functions on inputs

export function preventNonNumericalInput(e) {
  if (e.key.length === 1 && /\D/.test(e.key)) {
    e.preventDefault()
  }
}
