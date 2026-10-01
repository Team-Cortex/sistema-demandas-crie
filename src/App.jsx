import { BrowserRouter, Routes, Route } from 'react-router-dom';

// Exemplo de componentes de páginas
const Home = () => <h1>Página Inicial</h1>;
const About = () => <h1>Sobre</h1>;

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
