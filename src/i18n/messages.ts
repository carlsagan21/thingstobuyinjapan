import type { Category, Language } from '../types'

export const LANGUAGES: readonly Language[] = ['ko', 'en', 'ja'] as const

export const LANGUAGE_NAMES: Record<Language, string> = {
  ko: '한국어',
  en: 'English',
  ja: '日本語',
}

export interface Messages {
  title: string
  subtitle: string
  fxLabel: string
  fxLoading: string
  fxError: string
  filterAll: string
  countLabel: (n: number) => string
  sortLabel: string
  sortDefault: string
  sortMargin: string
  loading: string
  errorPrefix: string
  labelBuyPrice: string
  labelEstimatedPrice: string
  labelMargin: string
  labelBuyAt: string
  fxSourcePrefix: string
  disclaimer: string
  langSwitcherLabel: string
  category: Record<Category, string>
}

export const MESSAGES: Record<Language, Messages> = {
  ko: {
    title: '일본에서 사서 미국에서 팔기',
    subtitle: '일본 현지가와 미국 판매 예상가를 비교해 마진이 나오는 아이템 모음',
    fxLabel: '현재 환율',
    fxLoading: '환율 불러오는 중...',
    fxError: '환율 로드 실패',
    filterAll: '전체',
    countLabel: (n) => `${n}개`,
    sortLabel: '정렬',
    sortDefault: '기본순',
    sortMargin: '마진순',
    loading: '아이템 로딩 중...',
    errorPrefix: '에러:',
    labelBuyPrice: '구매가',
    labelEstimatedPrice: '예상 판매가',
    labelMargin: '예상 마진',
    labelBuyAt: '구매처:',
    fxSourcePrefix: '환율 데이터 출처:',
    disclaimer: '가격 정보는 참고용이며 실제 가격과 다를 수 있습니다.',
    langSwitcherLabel: '언어',
    category: {
      electronics: '전자제품',
      gaming: '게임',
      stationery: '문구',
      beauty: '뷰티',
      fashion: '패션',
      collectibles: '수집품',
      food: '식품',
      watches: '시계',
      kitchen: '주방',
    },
  },
  en: {
    title: 'Buy in Japan, Sell in the US',
    subtitle: 'Items with margin between Japan retail prices and US resale estimates',
    fxLabel: 'Exchange rate',
    fxLoading: 'Loading exchange rate...',
    fxError: 'Failed to load exchange rate',
    filterAll: 'All',
    countLabel: (n) => `${n} item${n === 1 ? '' : 's'}`,
    sortLabel: 'Sort',
    sortDefault: 'Default',
    sortMargin: 'Margin',
    loading: 'Loading items...',
    errorPrefix: 'Error:',
    labelBuyPrice: 'Buy price',
    labelEstimatedPrice: 'Est. resale',
    labelMargin: 'Est. margin',
    labelBuyAt: 'Where to buy:',
    fxSourcePrefix: 'FX data:',
    disclaimer: 'Prices are estimates for reference and may differ from actual market.',
    langSwitcherLabel: 'Language',
    category: {
      electronics: 'Electronics',
      gaming: 'Gaming',
      stationery: 'Stationery',
      beauty: 'Beauty',
      fashion: 'Fashion',
      collectibles: 'Collectibles',
      food: 'Food',
      watches: 'Watches',
      kitchen: 'Kitchen',
    },
  },
  ja: {
    title: '日本で買って、アメリカで売る',
    subtitle: '日本の店頭価格とアメリカでの推定転売価格を比較した、利幅のあるアイテム集',
    fxLabel: '現在の為替',
    fxLoading: '為替レート読み込み中...',
    fxError: '為替レートの読み込みに失敗',
    filterAll: 'すべて',
    countLabel: (n) => `${n}件`,
    sortLabel: '並び替え',
    sortDefault: '標準',
    sortMargin: '利幅順',
    loading: 'アイテム読み込み中...',
    errorPrefix: 'エラー:',
    labelBuyPrice: '購入価格',
    labelEstimatedPrice: '想定販売価格',
    labelMargin: '想定利益',
    labelBuyAt: '購入場所:',
    fxSourcePrefix: '為替データ提供:',
    disclaimer: '価格は参考値であり、実際の市場価格とは異なる場合があります。',
    langSwitcherLabel: '言語',
    category: {
      electronics: '家電',
      gaming: 'ゲーム',
      stationery: '文房具',
      beauty: '美容',
      fashion: 'ファッション',
      collectibles: 'コレクション',
      food: '食品',
      watches: '時計',
      kitchen: 'キッチン',
    },
  },
}
