import { useMemo, useState } from 'react'
import { useExchangeRate, useItems } from './hooks'
import type { Category, Item } from './types'
import './App.css'

const CATEGORY_LABELS: Record<Category, string> = {
  electronics: '전자제품',
  gaming: '게임',
  stationery: '문구',
  beauty: '뷰티',
  fashion: '패션',
  collectibles: '수집품',
  food: '식품',
  watches: '시계',
  kitchen: '주방',
}

type SortMode = 'default' | 'margin'

function App() {
  const items = useItems()
  const fx = useExchangeRate()
  const [selectedCategory, setSelectedCategory] = useState<Category | 'all'>('all')
  const [sortMode, setSortMode] = useState<SortMode>('default')

  const categories = useMemo(() => {
    if (!items.data) return []
    const set = new Set(items.data.map((i) => i.category))
    return Array.from(set)
  }, [items.data])

  const filtered = useMemo(() => {
    if (!items.data) return []
    if (selectedCategory === 'all') return items.data
    return items.data.filter((i) => i.category === selectedCategory)
  }, [items.data, selectedCategory])

  const sorted = useMemo(() => {
    if (sortMode === 'default') return filtered
    return [...filtered].sort(
      (a, b) =>
        b.estimatedPriceUsd / b.priceJpy - a.estimatedPriceUsd / a.priceJpy,
    )
  }, [filtered, sortMode])

  return (
    <div className="page">
      <header className="hero">
        <h1>일본에서 사서 미국에서 팔기</h1>
        <p className="subtitle">
          일본 현지가와 미국 판매 예상가를 비교해 마진이 나오는 아이템 모음
        </p>
        <FxBanner rate={fx.data?.rate ?? null} loading={fx.loading} error={fx.error} />
      </header>

      <nav className="filters">
        <FilterButton
          active={selectedCategory === 'all'}
          onClick={() => setSelectedCategory('all')}
        >
          전체
        </FilterButton>
        {categories.map((c) => (
          <FilterButton
            key={c}
            active={selectedCategory === c}
            onClick={() => setSelectedCategory(c)}
          >
            {CATEGORY_LABELS[c]}
          </FilterButton>
        ))}
      </nav>

      <main>
        {items.loading && <p className="status">아이템 로딩 중...</p>}
        {items.error && <p className="status error">에러: {items.error}</p>}
        {items.data && (
          <>
            <div className="toolbar">
              <span className="count">{sorted.length}개</span>
              <div className="sort">
                <span className="sort-label">정렬</span>
                <button
                  type="button"
                  className={sortMode === 'default' ? 'sort-btn active' : 'sort-btn'}
                  onClick={() => setSortMode('default')}
                >
                  기본순
                </button>
                <button
                  type="button"
                  className={sortMode === 'margin' ? 'sort-btn active' : 'sort-btn'}
                  onClick={() => setSortMode('margin')}
                >
                  마진순
                </button>
              </div>
            </div>
            <ul className="items">
              {sorted.map((item) => (
                <li key={item.id}>
                  <ItemCard item={item} usdPerJpy={fx.data?.rate ?? null} />
                </li>
              ))}
            </ul>
          </>
        )}
      </main>

      <footer className="footer">
        <p>
          환율 데이터 출처: <a href="https://frankfurter.dev" target="_blank">frankfurter.dev</a>
        </p>
        <p>가격 정보는 참고용이며 실제 가격과 다를 수 있습니다.</p>
      </footer>
    </div>
  )
}

function FilterButton({
  active,
  onClick,
  children,
}: {
  active: boolean
  onClick: () => void
  children: React.ReactNode
}) {
  return (
    <button
      type="button"
      className={active ? 'filter active' : 'filter'}
      onClick={onClick}
    >
      {children}
    </button>
  )
}

function FxBanner({
  rate,
  loading,
  error,
}: {
  rate: number | null
  loading: boolean
  error: string | null
}) {
  if (loading) return <div className="fx">환율 불러오는 중...</div>
  if (error || rate == null) return <div className="fx fx-error">환율 로드 실패</div>
  const jpyPerUsd = 1 / rate
  return (
    <div className="fx">
      현재 환율 <strong>1 USD = ¥{jpyPerUsd.toFixed(2)}</strong>
      <span className="fx-sub"> · 1 JPY = ${rate.toFixed(5)}</span>
    </div>
  )
}

function ItemCard({ item, usdPerJpy }: { item: Item; usdPerJpy: number | null }) {
  const buyCostUsd = usdPerJpy != null ? item.priceJpy * usdPerJpy : null
  const margin =
    buyCostUsd != null ? item.estimatedPriceUsd - buyCostUsd : null
  const marginPct =
    margin != null && buyCostUsd != null && buyCostUsd > 0
      ? (margin / buyCostUsd) * 100
      : null

  return (
    <article className="card">
      <div className="card-head">
        <h2>{item.name}</h2>
        {item.nameJp && <p className="name-jp">{item.nameJp}</p>}
      </div>

      <div className="prices">
        <div>
          <span className="label">구매가</span>
          <span className="value">¥{item.priceJpy.toLocaleString()}</span>
          {buyCostUsd != null && (
            <span className="usd">≈ ${buyCostUsd.toFixed(2)}</span>
          )}
        </div>
        <div>
          <span className="label">예상 판매가</span>
          <span className="value">${item.estimatedPriceUsd.toLocaleString()}</span>
        </div>
        {margin != null && marginPct != null && (
          <div className={marginPct > 0 ? 'margin pos' : 'margin neg'}>
            <span className="label">예상 마진</span>
            <span className="value">
              ${margin.toFixed(2)} ({marginPct.toFixed(0)}%)
            </span>
          </div>
        )}
      </div>

      <div className="meta">
        <p>
          <strong>구매처:</strong> {item.whereToBuy}
        </p>
        <p className="notes">{item.notes}</p>
      </div>
    </article>
  )
}

export default App
