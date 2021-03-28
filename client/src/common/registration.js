const VALIDATORS = [
  (str) => str.length >= 8,
  (str) => /[a-z]/i.test(str),
  (str) => /\d/.test(str),
  (str) => /\w/.test(str)
]

const MESSAGES = [
  { type: 'error', message: 'WEAK' },
  { type: 'error', message: 'WEAK' },
  { type: 'error', message: 'WEAK' },
  { type: 'warning', message: 'MEDIUM' },
  { type: 'success', message: 'STRONG' }
]

export function validatePass (pass) {
  const rating = VALIDATORS.reduce((acc, f) => f(pass) ? acc + 1 : acc, 0)

  return MESSAGES[rating]
}
