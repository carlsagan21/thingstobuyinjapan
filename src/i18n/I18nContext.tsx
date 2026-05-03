import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import type { ReactNode } from 'react'
import type { Language } from '../types'
import { LANGUAGES, MESSAGES, type Messages } from './messages'

const DEFAULT_LANG: Language = 'en'
const CANONICAL_ORIGIN = 'https://sookiwi.com'

const LOCALES: Record<Language, string> = {
  en: 'en_US',
  ko: 'ko_KR',
  ja: 'ja_JP',
}

function isLanguage(value: string): value is Language {
  return (LANGUAGES as readonly string[]).includes(value)
}

function getBase(): string {
  return import.meta.env.BASE_URL
}

function readLangFromPath(): Language {
  if (typeof window === 'undefined') return DEFAULT_LANG
  const base = getBase()
  const path = window.location.pathname
  const sub = path.startsWith(base) ? path.slice(base.length) : path
  const segment = sub.split('/')[0]
  if (segment && isLanguage(segment) && segment !== DEFAULT_LANG) return segment
  return DEFAULT_LANG
}

function pathForLang(lang: Language): string {
  const base = getBase()
  if (lang === DEFAULT_LANG) return base
  return `${base}${lang}/`
}

function writeLangToPath(lang: Language) {
  const targetPath = pathForLang(lang)
  const url = new URL(window.location.href)
  url.pathname = targetPath
  window.history.replaceState({}, '', url)
}

function setMetaContent(selector: string, value: string) {
  const el = document.querySelector(selector)
  if (el) el.setAttribute('content', value)
}

function setLinkHref(selector: string, value: string) {
  const el = document.querySelector(selector)
  if (el) el.setAttribute('href', value)
}

function syncDocumentMeta(lang: Language) {
  const m = MESSAGES[lang]
  const canonicalUrl = `${CANONICAL_ORIGIN}${pathForLang(lang)}`

  document.documentElement.lang = lang
  document.title = m.title

  setMetaContent('meta[name="description"]', m.subtitle)
  setLinkHref('link[rel="canonical"]', canonicalUrl)

  setMetaContent('meta[property="og:title"]', m.title)
  setMetaContent('meta[property="og:description"]', m.subtitle)
  setMetaContent('meta[property="og:url"]', canonicalUrl)
  setMetaContent('meta[property="og:locale"]', LOCALES[lang])
}

interface I18nContextValue {
  lang: Language
  setLang: (lang: Language) => void
  m: Messages
}

const I18nContext = createContext<I18nContextValue | null>(null)

export function I18nProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState<Language>(readLangFromPath)

  useEffect(() => {
    syncDocumentMeta(lang)
  }, [lang])

  useEffect(() => {
    const onPopState = () => {
      setLangState(readLangFromPath())
    }
    window.addEventListener('popstate', onPopState)
    return () => window.removeEventListener('popstate', onPopState)
  }, [])

  const value = useMemo<I18nContextValue>(
    () => ({
      lang,
      setLang: (l) => {
        writeLangToPath(l)
        setLangState(l)
      },
      m: MESSAGES[lang],
    }),
    [lang],
  )

  return <I18nContext.Provider value={value}>{children}</I18nContext.Provider>
}

export function useI18n(): I18nContextValue {
  const ctx = useContext(I18nContext)
  if (!ctx) throw new Error('useI18n must be used within I18nProvider')
  return ctx
}
