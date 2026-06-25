import { useState, useEffect } from 'react';
import api from '../services/api';
import { BookOpen, PieChart, Activity, PlusCircle, ArrowRight, Award, Calendar, Sparkles } from 'lucide-react';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await api.get('/questions/dashboard-stats');
        setStats(response.data);
      } catch (error) {
        console.error("Failed to fetch stats", error);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-2 border-indigo-600 border-b-transparent"></div>
      </div>
    );
  }

  // Defensive mappings
  const totalQuestions = stats?.total_questions !== undefined ? stats.total_questions : (stats?.totalQuestions || 0);
  const topicDistribution = stats?.topic_distribution || stats?.topicDistribution || [];
  const recentQuestions = stats?.recent_questions || stats?.recentQuestions || [];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in">
      {/* Welcome Header */}
      <div className="mb-8 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-gradient-to-br from-indigo-600 via-indigo-600 to-violet-600 p-6 sm:p-8 rounded-2xl text-white shadow-lg shadow-indigo-100 relative overflow-hidden">
        <div className="absolute -right-10 -top-10 w-40 h-40 bg-white/5 rounded-full blur-2xl pointer-events-none"></div>
        <div className="absolute -left-10 -bottom-10 w-40 h-40 bg-white/5 rounded-full blur-2xl pointer-events-none"></div>
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight">Dashboard Overview</h1>
          <p className="text-indigo-100 mt-1.5 max-w-md font-medium">Welcome back! Track your study stats, auto-tag history, and explore concepts.</p>
        </div>
        <Link 
          to="/ask" 
          className="inline-flex items-center gap-2 bg-white text-indigo-700 px-5.5 py-3.5 rounded-xl font-bold hover:bg-indigo-50 transition shadow-md hover:shadow-lg active:scale-95 duration-150 cursor-pointer"
        >
          <PlusCircle className="w-5 h-5 text-indigo-600" /> Ask a Question
        </Link>
      </div>
      
      {/* Top Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-2xl shadow-sm border border-slate-150 p-6 flex items-center hover:shadow-md hover:border-indigo-100 transition duration-200">
          <div className="p-3.5 rounded-xl bg-blue-50 text-blue-600 mr-4.5 shadow-inner">
            <BookOpen className="h-6 w-6" />
          </div>
          <div>
            <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Total Questions</p>
            <p className="text-3xl font-black text-slate-900 mt-1">{totalQuestions}</p>
          </div>
        </div>
        
        <div className="bg-white rounded-2xl shadow-sm border border-slate-150 p-6 flex items-center hover:shadow-md hover:border-indigo-100 transition duration-200">
          <div className="p-3.5 rounded-xl bg-purple-50 text-purple-600 mr-4.5 shadow-inner">
            <PieChart className="h-6 w-6" />
          </div>
          <div>
            <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Topics Explored</p>
            <p className="text-3xl font-black text-slate-900 mt-1">{topicDistribution.length}</p>
          </div>
        </div>
        
        <div className="bg-white rounded-2xl shadow-sm border border-slate-150 p-6 flex items-center hover:shadow-md hover:border-indigo-100 transition duration-200">
          <div className="p-3.5 rounded-xl bg-emerald-50 text-emerald-600 mr-4.5 shadow-inner">
            <Activity className="h-6 w-6" />
          </div>
          <div>
            <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Activity Status</p>
            <p className="text-2xl font-black text-emerald-950 mt-1">
              {totalQuestions > 15 ? 'Expert Learner' : totalQuestions > 5 ? 'Active Learner' : 'Getting Started'}
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Topic Distribution Chart */}
        <div className="bg-white rounded-2xl shadow-sm border border-slate-150 p-6 flex flex-col justify-between hover:shadow-md transition duration-200">
          <div>
            <h2 className="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2">
              <Award className="w-5 h-5 text-indigo-600 animate-bounce" />
              Topic Mastery
            </h2>
            {topicDistribution.length > 0 ? (
              <div className="space-y-5.5">
                {topicDistribution.map((item, index) => {
                  const percentage = totalQuestions > 0 ? (item.count / totalQuestions) * 100 : 0;
                  return (
                    <div key={index}>
                      <div className="flex justify-between text-sm font-semibold text-slate-700 mb-2">
                        <span className="capitalize">{item.topic}</span>
                        <span className="text-indigo-600 font-bold">{item.count} {item.count === 1 ? 'Question' : 'Questions'} ({percentage.toFixed(0)}%)</span>
                      </div>
                      <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
                        <div 
                          className="bg-indigo-600 h-full rounded-full transition-all duration-500 ease-out" 
                          style={{ width: `${percentage}%` }}
                        ></div>
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className="text-center py-12 text-slate-400 font-semibold italic">
                No topic data. Submit questions to build your chart.
              </div>
            )}
          </div>
        </div>

        {/* Recent Questions List */}
        <div className="bg-white rounded-2xl shadow-sm border border-slate-150 p-6 flex flex-col justify-between hover:shadow-md transition duration-200">
          <div>
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-indigo-600" />
                Recent Questions
              </h2>
              {recentQuestions.length > 0 && (
                <Link to="/history" className="text-xs font-bold text-indigo-600 hover:text-indigo-850 flex items-center gap-1">
                  View All <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              )}
            </div>
            
            {recentQuestions.length > 0 ? (
              <div className="space-y-4">
                {recentQuestions.map((q) => {
                  const qId = q.id || q._id;
                  const qDate = q.createdAt || q.created_at;
                  return (
                    <div key={qId} className="border-l-4 border-indigo-600 pl-4 py-2 bg-slate-50/50 rounded-r-xl pr-3 hover:bg-slate-50 transition duration-150 border-y border-r border-slate-150">
                      <p className="text-slate-800 font-bold mb-2 line-clamp-2">{q.question}</p>
                      <div className="flex items-center text-xs text-slate-500 gap-2 font-medium">
                        <span className="bg-indigo-50 border border-indigo-100 px-2.5 py-0.5 rounded-full text-indigo-700 font-bold uppercase tracking-wider text-[10px]">
                          {q.topic}
                        </span>
                        {q.confidence !== undefined && q.confidence !== null && (
                          <>
                            <span>•</span>
                            <span className="text-[10px] font-bold text-green-700 bg-green-50 border border-green-100 px-1.5 py-0.5 rounded uppercase tracking-wider">
                              {q.confidence}% Conf
                            </span>
                          </>
                        )}
                        <span>•</span>
                        <span className="flex items-center gap-1">
                          <Calendar className="w-3 h-3" />
                          {qDate ? new Date(qDate).toLocaleDateString() : 'N/A'}
                        </span>
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className="text-center py-12 text-slate-400 font-semibold italic">
                No recent activity. Ask a question to get started!
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
