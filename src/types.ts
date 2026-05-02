export type Category =
  | 'electronics'
  | 'gaming'
  | 'stationery'
  | 'beauty'
  | 'fashion'
  | 'collectibles'
  | 'food'
  | 'watches'

export interface Item {
  id: string
  name: string
  nameJp?: string
  category: Category
  priceJpy: number
  estimatedPriceUsd: number
  whereToBuy: string
  notes: string
  imageUrl?: string
}

export interface ExchangeRate {
  rate: number
  fetchedAt: string
}
