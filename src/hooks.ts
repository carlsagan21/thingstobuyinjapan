import { useEffect, useState } from 'react'
import type { ExchangeRate, Item } from './types'

interface AsyncState<T> {
  data: T | null
  loading: boolean
  error: string | null
}

export function useItems(): AsyncState<Item[]> {
  const [state, setState] = useState<AsyncState<Item[]>>({
    data: null,
    loading: true,
    error: null,
  })

  useEffect(() => {
    const url = `${import.meta.env.BASE_URL}data/items.json`
    fetch(url)
      .then((res) => {
        if (!res.ok) throw new Error(`Failed to load items (${res.status})`)
        return res.json() as Promise<Item[]>
      })
      .then((data) => setState({ data, loading: false, error: null }))
      .catch((err: unknown) => {
        const message = err instanceof Error ? err.message : 'Unknown error'
        setState({ data: null, loading: false, error: message })
      })
  }, [])

  return state
}

export function useExchangeRate(): AsyncState<ExchangeRate> {
  const [state, setState] = useState<AsyncState<ExchangeRate>>({
    data: null,
    loading: true,
    error: null,
  })

  useEffect(() => {
    fetch('https://api.frankfurter.dev/v1/latest?base=JPY&symbols=USD')
      .then((res) => {
        if (!res.ok) throw new Error(`FX API error (${res.status})`)
        return res.json() as Promise<{ rates: { USD: number }; date: string }>
      })
      .then((json) => {
        setState({
          data: { rate: json.rates.USD, fetchedAt: json.date },
          loading: false,
          error: null,
        })
      })
      .catch((err: unknown) => {
        const message = err instanceof Error ? err.message : 'Unknown error'
        setState({ data: null, loading: false, error: message })
      })
  }, [])

  return state
}
