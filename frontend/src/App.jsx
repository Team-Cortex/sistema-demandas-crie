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
import Auditoria from './pages/auditoria/Auditoria'
import Usuarios from './pages/usuarios/Usuarios'
import FormularioUsuario from './pages/usuarios/FormularioUsuario'
import FormEvolucao from './pages/evolucoes/FormEvolucao'
import VersoesEvolucao from './pages/evolucoes/VersoesEvolucao'
import Encaminhamentos from './pages/encaminhamentos/Encaminhamentos'
import RegistrarEncaminhamento from './pages/encaminhamentos/RegistrarEncaminhamento'
import RegistrarDesfecho from './pages/encaminhamentos/RegistrarDesfecho'
import Assistidos from './pages/assistidos/Assistidos'
import FormAssistido from './pages/assistidos/FormAssistido'
import FichaAssistido from './pages/assistidos/FichaAssistido'
import Reunioes from './pages/reunioes/Reunioes'
import FormularioReuniao from './pages/reunioes/FormularioReuniao'
import FichaReuniao from './pages/reunioes/FichaReuniao'

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
          { path: 'assistidos/:assistidoId/evolucoes/nova', element: <FormEvolucao /> },
          { path: 'evolucoes/:id', element: <VersoesEvolucao /> },
          { path: 'evolucoes/:id/retificar', element: <FormEvolucao /> },
          { path: 'encaminhamentos', element: <Encaminhamentos /> },
          { path: 'encaminhamentos/novo', element: <RegistrarEncaminhamento /> },
          { path: 'encaminhamentos/:id/desfecho', element: <RegistrarDesfecho /> },
          { path: 'assistidos', element: <Assistidos /> },
          { path: 'assistidos/novo', element: <FormAssistido /> },
          { path: 'assistidos/:id', element: <FichaAssistido /> },
          { path: 'assistidos/:id/editar', element: <FormAssistido /> },
          { path: 'reunioes', element: <Reunioes /> },
          { path: 'reunioes/nova', element: <FormularioReuniao /> },
          { path: 'reunioes/:id', element: <FichaReuniao /> },
          { path: 'reunioes/:id/editar', element: <FormularioReuniao /> },
          {
            element: <SomenteDirecao />,
            children: [
              { path: 'usuarios', element: <Usuarios /> },
              { path: 'usuarios/novo', element: <FormularioUsuario /> },
              { path: 'usuarios/:id/editar', element: <FormularioUsuario /> },
              { path: 'auditoria', element: <Auditoria /> },
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
