import { useContext, useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { BrainCircuit, LogOut, Home, History, PlusCircle, Cpu, ShieldCheck } from 'lucide-react';

const Navbar = () => {
  const { user, logout } = useContext(AuthContext);
  const location = useLocation();
  const [selectedModel, setSelectedModel] = useState('MiniLM Embedding Model');

  useEffect(() => {
    const savedModel = localStorage.getItem('selectedModel');
    if (savedModel) {
      setSelectedModel(savedModel);
    } else {
      localStorage.setItem('selectedModel', 'MiniLM Embedding Model');
    }
  }, []);

  const handleModelChange = (e) => {
    const newModel = e.target.value;
    setSelectedModel(newModel);
    localStorage.setItem('selectedModel', newModel);
    window.dispatchEvent(new Event('modelChanged'));
  };

  if (!user) return null;

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="bg-white/80 backdrop-blur-md border-b border-slate-150 sticky top-0 z-50 shadow-sm transition-all duration-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center gap-8">
            <Link to="/dashboard" className="flex items-center gap-2 group">
              <div className="bg-indigo-600 p-2 rounded-xl text-white shadow-sm shadow-indigo-100 group-hover:scale-105 transition duration-150">
                <BrainCircuit className="h-5.5 w-5.5" />
              </div>
              <span className="font-black text-xl text-slate-900 tracking-tight hidden sm:block">SmartQ</span>
            </Link>
            
            <div className="hidden sm:flex sm:space-x-2">
              <Link 
                to="/dashboard" 
                className={`inline-flex items-center px-3.5 py-2 text-sm font-bold rounded-xl gap-2 transition duration-150 ${
                  isActive('/dashboard') 
                    ? 'bg-indigo-50 text-indigo-750 border border-indigo-100/50' 
                    : 'text-slate-650 hover:text-slate-900 hover:bg-slate-50'
                }`}
              >
                <Home className="w-4 h-4" /> Dashboard
              </Link>
              <Link 
                to="/ask" 
                className={`inline-flex items-center px-3.5 py-2 text-sm font-bold rounded-xl gap-2 transition duration-150 ${
                  isActive('/ask') 
                    ? 'bg-indigo-50 text-indigo-750 border border-indigo-100/50' 
                    : 'text-slate-650 hover:text-slate-900 hover:bg-slate-50'
                }`}
              >
                <PlusCircle className="w-4 h-4" /> Ask Question
              </Link>
              <Link 
                to="/history" 
                className={`inline-flex items-center px-3.5 py-2 text-sm font-bold rounded-xl gap-2 transition duration-150 ${
                  isActive('/history') 
                    ? 'bg-indigo-50 text-indigo-750 border border-indigo-100/50' 
                    : 'text-slate-650 hover:text-slate-900 hover:bg-slate-50'
                }`}
              >
                <History className="w-4 h-4" /> History
              </Link>
              {user?.role === 'admin' && (
                <Link 
                  to="/admin" 
                  className={`inline-flex items-center px-3.5 py-2 text-sm font-bold rounded-xl gap-2 transition duration-150 ${
                    isActive('/admin') 
                      ? 'bg-indigo-50 text-indigo-750 border border-indigo-100/50' 
                      : 'text-slate-650 hover:text-slate-900 hover:bg-slate-50'
                  }`}
                >
                  <ShieldCheck className="w-4 h-4 text-indigo-600" /> Admin
                </Link>
              )}
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            {/* AI Model Selector */}
            <div className="flex items-center bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 gap-2 shadow-inner">
              <Cpu className="w-4 h-4 text-indigo-600" />
              <select
                id="modelSelect"
                value={selectedModel}
                onChange={handleModelChange}
                className="bg-transparent border-none text-xs font-bold text-slate-700 focus:ring-0 cursor-pointer outline-none"
              >
                <option value="MiniLM Embedding Model">MiniLM Model</option>
                <option value="Future AI Models">Future AI Models</option>
              </select>
            </div>

            <button
              onClick={logout}
              className="inline-flex items-center px-3.5 py-2 border border-slate-200 text-sm font-bold rounded-xl text-slate-600 hover:text-red-650 hover:bg-red-50 hover:border-red-100 transition duration-150 shadow-sm cursor-pointer"
            >
              <LogOut className="w-4 h-4 mr-1.5" />
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
