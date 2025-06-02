import { Link, useLocation } from 'react-router-dom'

const Navbar = () => {
  const location = useLocation()
  
  return (
    <nav className="bg-blue-600 shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center py-4">
          <div className="text-white font-bold text-xl">
            Nine Dash Line Detection
          </div>
          <div className="space-x-4">
            <NavLink to="/" active={location.pathname === "/"}>
              Home
            </NavLink>
            <NavLink to="/about" active={location.pathname === "/about"}>
              About
            </NavLink>
          </div>
        </div>
      </div>
    </nav>
  )
}

const NavLink = ({ to, active, children }) => {
  return (
    <Link
      to={to}
      className={`px-3 py-2 rounded-md text-sm font-medium ${
        active
          ? 'bg-blue-700 text-white'
          : 'text-white hover:bg-blue-500 hover:text-white'
      }`}
    >
      {children}
    </Link>
  )
}

export default Navbar
