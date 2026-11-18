import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import RootLayout from './components/layouts/RootLayout'
import Entrar from './pages/Entrar'
import ErrorPage from './pages/ErrorPage'
import Painel from './pages/Painel'
import MinhasDemandas from './pages/MinhasDemandas'
import Demandas from './pages/Demandas'
import NovaDemanda from './pages/NovaDemanda'
import DetalheDemanda from './pages/DetalheDemanda'
import SomenteDirecao from './components/layouts/SomenteDirecao'
import Relatorios from './pages/relatorios/Relatorios'

const rotas = createBrowserRouter([
  {
    errorElement: <ErrorPage />,
    children: [
      { path: '/entrar', element: <Entrar /> },
      {
        path: '/',
        element: <RootLayout />,
        children: [
          { index: true, element: <Painel /> },
          { path: 'minhas', element: <MinhasDemandas /> },
          { path: 'demandas', element: <Demandas /> },
          { path: 'demandas/nova', element: <NovaDemanda /> },
          { path: 'demandas/:id', element: <DetalheDemanda /> },
          {
            element: <SomenteDirecao />,
            children: [
              { path: 'relatorios', element: <Relatorios /> },
            ],
          },
        ],
      },
    ],
  },
])

export default function App() {
  return <RouterProvider router={rotas} />
}
