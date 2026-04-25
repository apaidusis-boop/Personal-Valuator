import { NavLink, Route, Routes, Navigate } from 'react-router-dom';
import { Portfolio } from './routes/Portfolio';
import { Ticker } from './routes/Ticker';
import { Agents } from './routes/Agents';
import './App.css';

const NAV = [
  { to: '/portfolio', label: 'Portfolio' },
  { to: '/ticker',    label: 'Ticker' },
  { to: '/agents',    label: 'Agents' },
];

export function App() {
  return (
    <div className="app-shell">
      <aside className="app-sidebar">
        <div className="brand">
          <div className="brand__name">Investment Intelligence</div>
          <div className="brand__caption">BR · US · DRIP</div>
        </div>
        <nav>
          {NAV.map(({ to, label }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `nav-link${isActive ? ' nav-link--active' : ''}`
              }
            >
              {label}
            </NavLink>
          ))}
        </nav>
        <div className="sidebar-footer">
          <div className="sidebar-footer__label">Powered by</div>
          <div className="sidebar-footer__value">Helena Mega · v0.1</div>
        </div>
      </aside>

      <main className="app-main">
        <Routes>
          <Route path="/" element={<Navigate to="/portfolio" replace />} />
          <Route path="/portfolio" element={<Portfolio />} />
          <Route path="/ticker" element={<Ticker />} />
          <Route path="/ticker/:symbol" element={<Ticker />} />
          <Route path="/agents" element={<Agents />} />
        </Routes>
      </main>
    </div>
  );
}
