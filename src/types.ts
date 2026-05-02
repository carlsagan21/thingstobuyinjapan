export type Language = 'ko' | 'en' | 'ja'

export interface LocalizedString {
  ko: string
  en: string
  ja: string
}

export type Category =
  | 'electronics'
  | 'gaming'
  | 'stationery'
  | 'beauty'
  | 'fashion'
  | 'collectibles'
  | 'food'
  | 'watches'
  | 'kitchen'

export interface Item {
  id: string
  name: LocalizedString
  category: Category
  priceJpy: number
  estimatedPriceUsd: number
  whereToBuy: LocalizedString
  notes: LocalizedString
}

export interface ExchangeRate {
  rate: number
  fetchedAt: string
}
