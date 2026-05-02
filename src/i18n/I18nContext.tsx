import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import type { ReactNode } from 'react'
import type { Language } from '../types'
import { LANGUAGES, MESSAGES, type Messages } from './messages'

const URL_PARAM = 'lang'
const DEFAULT_LANG: Language = 'en'

function isLanguage(value: string | null): value is Language {
  return value != null && (LANGUAGES as readonly string[]).includes(value)
}

function readLangFromUrl(): Language | null {
  if (typeof window === 'undefined') return null
  const value = new URLSearchParams(window.location.search).get(URL_PARAM)
  return isLanguage(value) ? value : null
}

function writeLangToUrl(lang: Language) {
  const url = new URL(window.location.href)
  if (lang === DEFAULT_LANG) {
    url.searchParams.delete(URL_PARAM)
  } else {
    url.searchParams.set(URL_PARAM, lang)
  }
  window.history.replaceState({}, '', url)
}

interface I18nContextValue {
  lang: Language
  setLang: (lang: Language) => void
  m: Messages
}

const I18nContext = createContext<I18nContextValue | null>(null)

export function I18nProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState<Language>(() => readLangFromUrl() ?? DEFAULT_LANG)

  useEffect(() => {
    document.documentElement.lang = lang
  }, [lang])

  useEffect(() => {
    const onPopState = () => {
      setLangState(readLangFromUrl() ?? DEFAULT_LANG)
    }
    window.addEventListener('popstate', onPopState)
    return () => window.removeEventListener('popstate', onPopState)
  }, [])

  const value = useMemo<I18nContextValue>(
    () => ({
      lang,
      setLang: (l) => {
        writeLangToUrl(l)
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
