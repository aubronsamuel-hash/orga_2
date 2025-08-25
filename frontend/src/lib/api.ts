export async function apiGet(path: string) {
  const url = (import.meta.env.VITE_API_URL || 'http://localhost:8000') + path
  const res = await fetch(url)
  return res.json()
}
