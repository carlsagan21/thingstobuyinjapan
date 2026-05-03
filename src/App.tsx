import { useMemo, useState } from 'react'
import { useExchangeRate, useItems } from './hooks'
import type { Category, Item, Language } from './types'
import { useI18n } from './i18n/I18nContext'
import { LANGUAGES, LANGUAGE_NAMES } from './i18n/messages'
import './App.css'

type SortMode = 'default' | 'margin'

function App() {
  const items = useItems()
  const fx = useExchangeRate()
  const { lang, m } = useI18n()
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
      <div className="topbar">
        <LanguageSwitcher />
      </div>

      <header className="hero">
        <h1>{m.title}</h1>
        <p className="subtitle">{m.subtitle}</p>
        <FxBanner rate={fx.data?.rate ?? null} loading={fx.loading} error={fx.error} />
      </header>

      <nav className="filters">
        <FilterButton
          active={selectedCategory === 'all'}
          onClick={() => setSelectedCategory('all')}
        >
          {m.filterAll}
        </FilterButton>
        {categories.map((c) => (
          <FilterButton
            key={c}
            active={selectedCategory === c}
            onClick={() => setSelectedCategory(c)}
          >
            {m.category[c]}
          </FilterButton>
        ))}
      </nav>

      <main>
        {items.loading && <p className="status">{m.loading}</p>}
        {items.error && (
          <p className="status error">
            {m.errorPrefix} {items.error}
          </p>
        )}
        {items.data && (
          <>
            <div className="toolbar">
              <span className="count">{m.countLabel(sorted.length)}</span>
              <div className="sort">
                <span className="sort-label">{m.sortLabel}</span>
                <button
                  type="button"
                  className={sortMode === 'default' ? 'sort-btn active' : 'sort-btn'}
                  onClick={() => setSortMode('default')}
                >
                  {m.sortDefault}
                </button>
                <button
                  type="button"
                  className={sortMode === 'margin' ? 'sort-btn active' : 'sort-btn'}
                  onClick={() => setSortMode('margin')}
                >
                  {m.sortMargin}
                </button>
              </div>
            </div>
            <ul className="items">
              {sorted.map((item) => (
                <li key={item.id}>
                  <ItemCard item={item} usdPerJpy={fx.data?.rate ?? null} lang={lang} />
                </li>
              ))}
            </ul>
          </>
        )}
      </main>

      <footer className="footer">
        <p>
          {m.fxSourcePrefix}{' '}
          <a href="https://frankfurter.dev" target="_blank" rel="noreferrer">
            frankfurter.dev
          </a>
        </p>
        <p>{m.disclaimer}</p>
      </footer>
    </div>
  )
}

function LanguageSwitcher() {
  const { lang, setLang, m } = useI18n()
  return (
    <div className="lang-switcher" role="group" aria-label={m.langSwitcherLabel}>
      {LANGUAGES.map((l) => (
        <button
          key={l}
          type="button"
          className={l === lang ? 'lang-btn active' : 'lang-btn'}
          onClick={() => setLang(l)}
          aria-pressed={l === lang}
        >
          {LANGUAGE_NAMES[l]}
        </button>
      ))}
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
  const { m } = useI18n()
  if (loading) return <div className="fx">{m.fxLoading}</div>
  if (error || rate == null) return <div className="fx fx-error">{m.fxError}</div>
  const jpyPerUsd = 1 / rate
  return (
    <div className="fx">
      {m.fxLabel} <strong>1 USD = ¥{jpyPerUsd.toFixed(2)}</strong>
      <span className="fx-sub"> · 1 JPY = ${rate.toFixed(5)}</span>
    </div>
  )
}

function ItemCard({
  item,
  usdPerJpy,
  lang,
}: {
  item: Item
  usdPerJpy: number | null
  lang: Language
}) {
  const { m } = useI18n()
  const buyCostUsd = usdPerJpy != null ? item.priceJpy * usdPerJpy : null
  const margin =
    buyCostUsd != null ? item.estimatedPriceUsd - buyCostUsd : null
  const marginPct =
    margin != null && buyCostUsd != null && buyCostUsd > 0
      ? (margin / buyCostUsd) * 100
      : null

  const showJpSubtitle = lang !== 'ja'

  return (
    <article className="card">
      <div className="card-head">
        <h2>{item.name[lang]}</h2>
        {showJpSubtitle && <p className="name-jp">{item.name.ja}</p>}
      </div>

      <div className="prices">
        <div>
          <span className="label">{m.labelBuyPrice}</span>
          <span className="value">¥{item.priceJpy.toLocaleString()}</span>
          {buyCostUsd != null && (
            <span className="usd">≈ ${buyCostUsd.toFixed(2)}</span>
          )}
        </div>
        <div>
          <span className="label">{m.labelEstimatedPrice}</span>
          <span className="value">${item.estimatedPriceUsd.toLocaleString()}</span>
        </div>
        {margin != null && marginPct != null && (
          <div className={marginPct > 0 ? 'margin pos' : 'margin neg'}>
            <span className="label">{m.labelMargin}</span>
            <span className="value">
              ${margin.toFixed(2)} ({marginPct.toFixed(0)}%)
            </span>
          </div>
        )}
      </div>

      <div className="meta">
        <p>
          <strong>{m.labelBuyAt}</strong> {item.whereToBuy[lang]}
        </p>
        <p className="notes">{item.notes[lang]}</p>
      </div>
    </article>
  )
}

export default App
