import { useState, useEffect, useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import api from '../services/api';
import { 
  ShieldCheck, Loader2, Sparkles, Tag, PlusCircle, CheckCircle2, 
  AlertCircle, FileText, Search, ArrowUpDown, Trash2, Database, HelpCircle
} from 'lucide-react';

const Admin = () => {
  const { user } = useContext(AuthContext);
  
  // Guard route for Admin role only
  if (user?.role !== 'admin') {
    return <Navigate to="/dashboard" replace />;
  }

  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [successMsg, setSuccessMsg] = useState('');
  const [selectedCandidate, setSelectedCandidate] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState('Technology');
  const [submitting, setSubmitting] = useState(false);

  // Search & Filter state
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState('hits_desc'); // hits_desc, name_asc

  // Stats
  const [stats, setStats] = useState({
    totalActiveTopics: 0,
    totalQuestions: 0
  });

  // Fetch metrics & pending topics
  const fetchAdminData = async () => {
    setLoading(true);
    try {
      const pendingResponse = await api.get('/discovered-topics?status_filter=pending');
      setCandidates(pendingResponse.data);

      // Fetch active topics to display counts
      const activeTopicsRes = await api.get('/topics?format=objects');
      
      // Count total global questions in database for Memory Catalog
      let questionsCount = 0;
      try {
        const globalStatsRes = await api.get('/questions/global-stats');
        questionsCount = globalStatsRes.data?.total_questions ?? 0;
      } catch (e) {
        const questionsRes = await api.get('/questions/history');
        questionsCount = Array.isArray(questionsRes.data) ? questionsRes.data.length : 0;
      }

      setStats({
        totalActiveTopics: Array.isArray(activeTopicsRes.data) ? activeTopicsRes.data.length : 17,
        totalQuestions: questionsCount
      });
    } catch (err) {
      setError('Failed to fetch panel metrics. Please check server connections.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAdminData();
  }, []);

  const handleOpenApproveModal = (candidate) => {
    setSelectedCandidate(candidate);
    setSelectedCategory('Technology');
    setError('');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleApprove = async () => {
    if (!selectedCandidate) return;
    setSubmitting(true);
    setError('');
    setSuccessMsg('');

    try {
      const candidateId = selectedCandidate._id || selectedCandidate.id;
      const response = await api.post(
        `/discovered-topics/${candidateId}/approve?category=${selectedCategory}`
      );
      setSuccessMsg(`Successfully promoted and approved topic "${response.data.name}"!`);
      setSelectedCandidate(null);
      fetchAdminData();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to approve discovered topic.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleReject = async (id, name) => {
    if (!window.confirm(`Are you sure you want to dismiss the topic candidate "${name}"?`)) {
      return;
    }
    setError('');
    setSuccessMsg('');

    try {
      await api.post(`/discovered-topics/${id}/reject`);
      setSuccessMsg(`Successfully dismissed candidate topic "${name}".`);
      if (selectedCandidate && (selectedCandidate._id === id || selectedCandidate.id === id)) {
        setSelectedCandidate(null);
      }
      fetchAdminData();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to reject discovered topic.');
    }
  };

  // Filter and sort candidates
  const filteredCandidates = candidates
    .filter(c => {
      const query = searchQuery.toLowerCase();
      const nameMatch = c.name.toLowerCase().includes(query);
      const keywordMatch = (c.keywords || []).some(k => k.toLowerCase().includes(query));
      return nameMatch || keywordMatch;
    })
    .sort((a, b) => {
      if (sortBy === 'hits_desc') {
        const hitsA = a.questionCount || a.question_count || 0;
        const hitsB = b.questionCount || b.question_count || 0;
        return hitsB - hitsA;
      } else {
        return a.name.localeCompare(b.name);
      }
    });

  // Calculate sum of question hits across pending discoveries
  const totalPendingHits = candidates.reduce((sum, c) => sum + (c.questionCount || c.question_count || 1), 0);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in">
      {/* Header */}
      <div className="mb-8 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-gradient-to-br from-indigo-600 via-indigo-600 to-violet-600 p-6 sm:p-8 rounded-2xl text-white shadow-lg shadow-indigo-100 relative overflow-hidden">
        <div className="absolute -right-10 -top-10 w-40 h-40 bg-white/5 rounded-full blur-2xl pointer-events-none"></div>
        <div className="absolute -left-10 -bottom-10 w-40 h-40 bg-white/5 rounded-full blur-2xl pointer-events-none"></div>
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight flex items-center gap-2">
            <ShieldCheck className="h-8 w-8 text-white" />
            AI Admin Panel
          </h1>
          <p className="text-indigo-100 mt-1.5 max-w-xl font-medium">
            Analyze, curate, and promote AI-discovered categories to optimize search mapping accuracy.
          </p>
        </div>
        <button 
          onClick={fetchAdminData}
          className="inline-flex items-center gap-2 bg-white text-indigo-700 px-5.5 py-3.5 rounded-xl font-bold hover:bg-indigo-50 transition shadow-md hover:shadow-lg active:scale-95 duration-150 cursor-pointer"
        >
          Refresh Panel
        </button>
      </div>

      {/* Analytics stats dashboard */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-2xl shadow-sm border border-slate-150 p-6 flex items-center hover:shadow-md hover:border-indigo-100 transition duration-200">
          <div className="p-3.5 rounded-xl bg-indigo-50 text-indigo-600 mr-4.5 shadow-inner">
            <Sparkles className="h-6 w-6" />
          </div>
          <div>
            <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Pending Topics</p>
            <p className="text-3xl font-black text-slate-900 mt-1">{candidates.length}</p>
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow-sm border border-slate-150 p-6 flex items-center hover:shadow-md hover:border-indigo-100 transition duration-200">
          <div className="p-3.5 rounded-xl bg-purple-50 text-purple-600 mr-4.5 shadow-inner">
            <HelpCircle className="h-6 w-6" />
          </div>
          <div>
            <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Unclassified Hits</p>
            <p className="text-3xl font-black text-slate-900 mt-1">{totalPendingHits}</p>
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow-sm border border-slate-150 p-6 flex items-center hover:shadow-md hover:border-indigo-100 transition duration-200">
          <div className="p-3.5 rounded-xl bg-emerald-50 text-emerald-600 mr-4.5 shadow-inner">
            <Database className="h-6 w-6" />
          </div>
          <div>
            <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Active Vocabularies</p>
            <p className="text-3xl font-black text-slate-900 mt-1">{stats.totalActiveTopics}</p>
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow-sm border border-slate-150 p-6 flex items-center hover:shadow-md hover:border-indigo-100 transition duration-200">
          <div className="p-3.5 rounded-xl bg-blue-50 text-blue-600 mr-4.5 shadow-inner">
            <FileText className="h-6 w-6" />
          </div>
          <div>
            <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Memory Catalog</p>
            <p className="text-3xl font-black text-slate-900 mt-1">{stats.totalQuestions}</p>
          </div>
        </div>
      </div>

      {successMsg && (
        <div className="mb-6 flex items-start gap-2 text-sm text-green-700 bg-green-50 p-4 rounded-xl border border-green-200 shadow-sm animate-fade-in-up">
          <CheckCircle2 className="w-5 h-5 flex-shrink-0 mt-0.5 text-green-500" />
          <span className="font-semibold">{successMsg}</span>
        </div>
      )}

      {error && (
        <div className="mb-6 flex items-start gap-2 text-sm text-red-600 bg-red-50 p-4 rounded-xl border border-red-150 shadow-sm">
          <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
          <span>{error}</span>
        </div>
      )}

      {/* Main interface layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left Column: List of candidates */}
        <div className="lg:col-span-2 space-y-6">
          <div className="flex flex-col sm:flex-row gap-4 items-center justify-between bg-white p-4 rounded-xl border border-gray-150 shadow-sm">
            {/* Search Box */}
            <div className="relative w-full sm:w-72">
              <Search className="absolute left-3 top-2.5 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search topic or keyword..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-gray-50 border border-gray-200 rounded-lg pl-9 pr-4 py-2 text-sm text-gray-800 focus:bg-white focus:border-indigo-500 outline-none transition"
              />
            </div>
            
            {/* Sort Dropdown */}
            <div className="flex items-center gap-2 w-full sm:w-auto justify-end">
              <ArrowUpDown className="w-4 h-4 text-gray-500" />
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="bg-white border border-gray-250 rounded-lg text-xs font-semibold text-gray-700 px-3 py-2 cursor-pointer focus:ring-0 outline-none"
              >
                <option value="hits_desc">Sort by Query Hits (High → Low)</option>
                <option value="name_asc">Sort by Name (A → Z)</option>
              </select>
            </div>
          </div>

          {loading ? (
            <div className="flex flex-col items-center justify-center py-20 bg-white rounded-2xl border border-gray-150 shadow-sm">
              <Loader2 className="w-10 h-10 animate-spin text-indigo-600 mb-4" />
              <p className="text-gray-500 font-semibold">Scanning MongoDB discover candidates...</p>
            </div>
          ) : filteredCandidates.length === 0 ? (
            <div className="bg-white rounded-2xl border border-gray-150 p-12 text-center shadow-sm">
              <Sparkles className="w-12 h-12 text-indigo-200 mx-auto mb-4" />
              <h3 className="text-lg font-bold text-gray-800 mb-1">No Matching Candidates</h3>
              <p className="text-gray-500 max-w-md mx-auto">
                No pending topic candidates fit your filter query. Adjust search text or refresh the board.
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {filteredCandidates.map((c) => {
                const cId = c._id || c.id;
                return (
                  <div 
                    key={cId} 
                    className="bg-white rounded-2xl border border-gray-150 p-5 shadow-sm hover:shadow-md hover:border-indigo-150 transition duration-150 flex flex-col justify-between"
                  >
                    <div>
                      <div className="flex items-center justify-between mb-3">
                        <span className="inline-flex items-center text-xs font-bold text-indigo-700 bg-indigo-50 border border-indigo-100 px-2.5 py-1 rounded-full uppercase tracking-wider">
                          Topic Candidate
                        </span>
                        <span className="text-xs text-gray-600 font-bold bg-gray-50 border border-gray-200 px-2.5 py-1 rounded-full">
                          {c.questionCount || c.question_count || 1} hits
                        </span>
                      </div>

                      <h3 className="text-lg font-bold text-gray-900 mb-2 capitalize">{c.name}</h3>

                      {/* Keywords list */}
                      <div className="mb-4">
                        <p className="text-xs text-gray-500 font-semibold uppercase tracking-wider mb-1.5">Extracted Keywords</p>
                        <div className="flex flex-wrap gap-1.5">
                          {(c.keywords || []).slice(0, 8).map((keyword, kidx) => (
                            <span key={kidx} className="inline-flex items-center text-xs text-gray-600 bg-gray-50 border border-gray-200 px-2 py-0.5 rounded-md">
                              {keyword}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>

                    <div className="flex gap-2 mt-4 pt-3 border-t border-gray-100">
                      <button
                        onClick={() => handleReject(cId, c.name)}
                        className="flex-1 inline-flex items-center justify-center px-3 py-2 border border-gray-200 text-xs font-bold rounded-lg text-red-600 hover:text-red-700 hover:bg-red-50 hover:border-red-200 transition cursor-pointer"
                      >
                        <Trash2 className="w-3.5 h-3.5 mr-1" /> Reject
                      </button>
                      <button
                        onClick={() => handleOpenApproveModal(c)}
                        className="flex-1 inline-flex items-center justify-center px-3 py-2 border border-transparent text-xs font-bold rounded-lg shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 transition cursor-pointer"
                      >
                        <PlusCircle className="w-3.5 h-3.5 mr-1" /> Promote
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Right Column: Approval/Promotion Widget */}
        <div className="lg:col-span-1">
          {selectedCandidate ? (
            <div className="bg-white border border-indigo-150 rounded-2xl p-6 shadow-md sticky top-24 animate-fade-in-up">
              <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                <Tag className="w-5 h-5 text-indigo-600" />
                Approve Promotion
              </h2>

              <div className="bg-indigo-50 border border-indigo-100 rounded-xl p-4 mb-5 text-sm">
                <p className="text-indigo-850 font-bold capitalize text-base mb-1">{selectedCandidate.name}</p>
                <p className="text-indigo-600">
                  Promoting this topic moves it into the active categorizer vocabularies, enabling immediate mapping to future student queries.
                </p>
              </div>

              <div className="mb-5">
                <label className="block text-sm font-bold text-gray-700 mb-2">
                  Assign Subject Category
                </label>
                <div className="grid grid-cols-2 gap-3">
                  <button
                    onClick={() => setSelectedCategory('Technology')}
                    className={`py-2 px-3 text-sm font-semibold rounded-lg border text-center transition ${
                      selectedCategory === 'Technology'
                        ? 'bg-indigo-600 border-indigo-600 text-white shadow-sm'
                        : 'bg-white border-gray-200 text-gray-700 hover:bg-gray-50'
                    }`}
                  >
                    Technology
                  </button>
                  <button
                    onClick={() => setSelectedCategory('Education')}
                    className={`py-2 px-3 text-sm font-semibold rounded-lg border text-center transition ${
                      selectedCategory === 'Education'
                        ? 'bg-indigo-600 border-indigo-600 text-white shadow-sm'
                        : 'bg-white border-gray-200 text-gray-700 hover:bg-gray-50'
                    }`}
                  >
                    Education
                  </button>
                </div>
              </div>

              <div className="flex gap-3">
                <button
                  onClick={() => setSelectedCandidate(null)}
                  disabled={submitting}
                  className="flex-1 py-2 px-4 border border-gray-200 text-sm font-semibold rounded-lg text-gray-700 bg-white hover:bg-gray-50 transition cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  onClick={handleApprove}
                  disabled={submitting}
                  className="flex-1 py-2 px-4 border border-transparent text-sm font-semibold rounded-lg shadow-sm text-white bg-green-600 hover:bg-green-700 disabled:opacity-50 transition flex items-center justify-center cursor-pointer"
                >
                  {submitting ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Confirm Approval'}
                </button>
              </div>
            </div>
          ) : (
            <div className="bg-gray-50 border border-gray-200 border-dashed rounded-2xl p-8 text-center sticky top-24">
              <FileText className="w-10 h-10 text-gray-400 mx-auto mb-3" />
              <h3 className="text-base font-bold text-gray-700 mb-1">Select a Candidate</h3>
              <p className="text-gray-500 text-sm">
                Click "Promote" on any pending topic discovery to review category allocation or assign it to a subject class.
              </p>
            </div>
          )}
        </div>

      </div>
    </div>
  );
};

export default Admin;
