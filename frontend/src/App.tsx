import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Missions from './pages/Missions'
import MissionDetail from './pages/MissionDetail'
import Technicians from './pages/Technicians'
import Calendar from './pages/Calendar'
import Login from './pages/Login'

export default function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Dashboard</Link> |
        <Link to="/missions">Missions</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/login" element={<Login />} />
        <Route path="/missions" element={<Missions />} />
        <Route path="/missions/:id" element={<MissionDetail />} />
        <Route path="/technicians" element={<Technicians />} />
        <Route path="/calendar" element={<Calendar />} />
      </Routes>
    </BrowserRouter>
  )
}
