import { useEffect, useState } from 'react'

export type ApiState<T> =
  | { kind: 'loading' }
  | { kind: 'error'; message: string }
  | { kind: 'ready'; data: T }

type Loader<T> = (signal: AbortSignal) => Promise<T>

const LOADING = { kind: 'loading' } as const

/**
 * Runs `load` whenever its identity changes and aborts the previous request.
 * Wrap `load` in useCallback so it only changes when its inputs change.
 */
export function useApi<T>(load: Loader<T>): ApiState<T> {
  // The settled state is tagged with the loader that produced it, so a new
  // loader reads as 'loading' without a synchronous setState in the effect.
  const [settled, setSettled] = useState<{ load: Loader<T>; state: ApiState<T> } | null>(null)

  useEffect(() => {
    const controller = new AbortController()
    load(controller.signal)
      .then((data) => setSettled({ load, state: { kind: 'ready', data } }))
      .catch((error: unknown) => {
        if (controller.signal.aborted) return
        const message = error instanceof Error ? error.message : String(error)
        setSettled({ load, state: { kind: 'error', message } })
      })
    return () => controller.abort()
  }, [load])

  return settled && settled.load === load ? settled.state : LOADING
}
