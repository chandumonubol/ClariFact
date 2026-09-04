import { AuthProvider } from './context/AuthContext'
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
  useNavigate,
  useLocation,
} from 'react-router-dom'
import HomePage from './pages/HomePage'
import RegisterPage from './pages/RegisterPage'
import LoginPage from './pages/LoginPage'
import DashboardPage from './pages/DashboardPage'
import AnalyzePage from './pages/AnalyzePage'
import ProcessingPage from './pages/ProcessingPage'
import ResultsPage from './pages/ResultsPage'
import HistoryPage from './pages/HistoryPage'
import AnalysisDetailPage from './pages/AnalysisDetailPage'
import './index.css'

function NavLink({ to, children, ...props }: { to: string; children: React.ReactNode; any }) {
  const navigate = useNavigate()
  const location = useLocation()

  const isActive = location.pathname === to || (location.pathname.startsWith(to) && location.pathname !== '/')

  return (
    <Link to={to} onClick={() => navigate(to)} className={`
      text-sm font-medium transition-colors ${isActive ? 'text-accent_primary' : 'text-text_secondary hover:text-accent_primary'}
    `} {...props}>
      {children}
    </Link>
  )
}

function NavMenu() {
  const { isAuthenticated, user, logout } = useAuth()

  return (
    <div className="flex items-center gap-3">
      {!isAuthenticated ? (
        <>
          <NavLink to="/register">Register</NavLink>
          <NavLink to="/login">Login</NavLink>
        </>
      ) : (
        <>
          <span className="text-sm text-text_secondary">
            Welcome, {user?.name || ''}
          </span>
          <NavLink to="/dashboard" className="font-medium">
            Dashboard
          </NavLink>
          <button
            onClick={() => logout()}
            className="px-3 py-1 text-sm text-accent_danger hover:text-red-600"
          >
            Logout
          </button>
        </>
      )}
    </div>
  )
}

export default function App() {
  return (
    <Router>
      <div className="min-h-screen bg-bg_light text-text_primary">
        <nav className="border-b border-border bg-white px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Link to="/" className="text-xl font-semibold">
              ClariFact
            </Link>
          </div>
          <div className="flex items-center gap-3">
            <NavMenu />
          </div>
        </nav>

        <main className="px-4 py-6">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/analyze" element={<AnalyzePage />} />
            <Route path="/processing" element={<ProcessingPage />} />
            <Route path="/results/:id" element={<ResultsPage />} />
            <Route path="/history" element={<HistoryPage />} />
            <Route path="/analysis/:id" element={<AnalysisDetailPage />} />
          </Routes>
        </main>

        <footer className="border-t border-border mt-6 py-4 text-sm text-text_secondary">
          <div className="text-center">
            © 2026 ClariFact. AI-assisted credibility assessment.
          </div>
        </footer>
      </div>
    </Router>
  )
}