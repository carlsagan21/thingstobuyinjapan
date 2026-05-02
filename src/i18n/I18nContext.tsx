import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import type { ReactNode } from 'react'
import type { Language } from '../types'
import { LANGUAGES, MESSAGES, type Messages } from './messages'

const STORAGE_KEY = 'lang'

function detectInitial(): Language {
  if (typeof window === 'undefined') return 'ko'
  const stored = window.localStorage.getItem(STORAGE_KEY)
  if (stored && (LANGUAGES as readonly string[]).includes(stored)) {
    return stored as Language
  }
  const browser = navigator.language.toLowerCase()
  if (browser.startsWith('ja')) return 'ja'
  if (browser.startsWith('en')) return 'en'
  return 'ko'
}

interface I18nContextValue {
  lang: Language
  setLang: (lang: Language) => void
  m: Messages
}

const I18nContext = createContext<I18nContextValue | null>(null)

export function I18nProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState<Language>(detectInitial)

  useEffect(() => {
    document.documentElement.lang = lang
  }, [lang])

  const value = useMemo<I18nContextValue>(
    () => ({
      lang,
      setLang: (l) => {
        window.localStorage.setItem(STORAGE_KEY, l)
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
