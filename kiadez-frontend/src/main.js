import { mount } from 'svelte'
import './app.css'
import App from './App.svelte'

const resolveDocumentLang = () => {
  if (typeof window === 'undefined') return 'es'
  const supported = new Set(['es', 'pt', 'en'])
  const langParam = new URLSearchParams(window.location.search).get('lang')
  const normalized = String(langParam || '').trim().toLowerCase()
  return supported.has(normalized) ? normalized : 'es'
}

if (typeof document !== 'undefined') {
  document.documentElement.lang = resolveDocumentLang()
}

const app = mount(App, {
  target: document.getElementById('app'),
})

if (typeof window !== 'undefined' && 'serviceWorker' in navigator && import.meta.env.PROD) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js').catch((error) => {
      console.warn('No se pudo registrar el service worker de Kiadez:', error)
    })
  })
}

export default app
