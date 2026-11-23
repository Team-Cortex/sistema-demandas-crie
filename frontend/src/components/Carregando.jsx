export default function Carregando({ children = 'Carregando…' }) {
  return <p role="status">{children}</p>
}
