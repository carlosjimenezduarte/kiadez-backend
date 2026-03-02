import { mount } from 'svelte'
import './app.css'
import App from './App.svelte'
import { getLocale } from './lib/i18n'

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/+$/, '') ||
  'http://127.0.0.1:8000'

const API_ORIGIN = (() => {
  if (typeof window === 'undefined') return ''
  try {
    return new URL(API_BASE_URL, window.location.origin).origin
  } catch {
    return ''
  }
})()

const shouldAttachLocaleHeader = (input) => {
  if (typeof window === 'undefined' || !API_ORIGIN) return false
  try {
    const rawUrl =
      typeof input === 'string'
        ? input
        : input instanceof Request
          ? input.url
          : String(input?.url || '')
    if (!rawUrl) return false
    const target = new URL(rawUrl, window.location.href)
    return target.origin === API_ORIGIN
  } catch {
    return false
  }
}

if (typeof window !== 'undefined' && typeof window.fetch === 'function') {
  if (!window.__kiadezLocaleFetchPatched) {
    const nativeFetch = window.fetch.bind(window)
    window.fetch = (input, init) => {
      if (!shouldAttachLocaleHeader(input)) {
        return nativeFetch(input, init)
      }

      const headers = new Headers(
        init?.headers ?? (input instanceof Request ? input.headers : undefined)
      )
      if (!headers.has('Accept-Language')) {
        headers.set('Accept-Language', getLocale())
      }

      return nativeFetch(input, {
        ...(init || {}),
        headers,
      })
    }
    window.__kiadezLocaleFetchPatched = true
  }
}

const app = mount(App, {
  target: document.getElementById('app'),
})

export default app
