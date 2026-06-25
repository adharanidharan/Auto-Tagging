import { useState, useEffect } from 'react';
import api from '../services/api';
import { Filter, Search, Tag, Calendar, HelpCircle, HistoryIcon } from 'lucide-react';

const History = () => {
  const [questions, setQuestions] = useState([]);
  const [topics, setTopics] = useState(['All']);
  const [loading, setLoading] = useState(true);
  const [filterTopic, setFilterTopic] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');

  // Load topics from the backend on mount
  useEffect(() => {
    const fetchTopics = async () => {
      try {
        const response = await api.get('/topics');
        setTopics(['All', ...response.data]);
      } catch (error) {
        console.error("Failed to fetch topics dynamically, using fallback", error);
        setTopics(['All', 'Biology', 'Physics', 'Mathematics', 'Computer Science', 'Chemistry', 'History', 'General']);
      }
    };
    fetchTopics();
  }, []);

  // Fetch history when topic filter changes
  useEffect(() => {
    const fetchHistory = async () => {
      setLoading(true);
      try {
        const url = filterTopic === 'All' ? '/questions/history' : `/questions/history?topic=${filterTopic}`;
        const response = await api.get(url);
        setQuestions(response.data);
      } catch (error) {
        console.error("Failed to fetch history", error);
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, [filterTopic]);

  // Client-side filtering of questions based on search query
  const filteredQuestions = questions.filter(q => 
    q.question.toLowerCase().includes(searchQuery.toLowerCase()) ||
    q.topic.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in">
      {/* Header */}
      <div className="mb-8 pb-5 border-b border-slate-100 flex items-center gap-3">
        <div className="bg-indigo-600 p-2.5 rounded-xl text-white shadow-sm">
          <HistoryIcon className="h-6 w-6" />
        </div>
        <div>
          <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">Your Question History</h1>
          <p className="text-slate-500 mt-1 font-medium">Review all your past study queries and their corresponding AI analysis.</p>
        </div>
      </div>

      {/* Filter and Search controls */}
      <div className="flex flex-col md:flex-row gap-4 mb-8 bg-white p-4 rounded-xl border border-slate-150 shadow-sm">
        {/* Search Input */}
        <div className="flex-1 flex items-center bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 focus-within:bg-white focus-within:ring-1 focus-within:ring-indigo-500 transition">
          <Search className="w-5 h-5 text-slate-400 mr-3" />
          <input
            type="text"
            placeholder="Search past questions by keyword or topic..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-transparent border-none outline-none text-sm text-slate-700 placeholder-slate-400 font-medium"
          />
        </div>

        {/* Topic Filter */}
        <div className="flex items-center bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 focus-within:bg-white focus-within:ring-1 focus-within:ring-indigo-500 transition min-w-[220px]">
          <Filter className="w-4 h-4 text-slate-400 mr-2" />
          <select
            value={filterTopic}
            onChange={(e) => setFilterTopic(e.target.value)}
            className="border-none bg-transparent focus:ring-0 text-sm font-bold text-slate-700 w-full outline-none cursor-pointer"
          >
            {topics.map(topic => (
              <option key={topic} value={topic}>{topic}</option>
            ))}
          </select>
        </div>
      </div>

      {loading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-2 border-indigo-600 border-b-transparent"></div>
        </div>
      ) : filteredQuestions.length > 0 ? (
        <div className="space-y-6">
          {filteredQuestions.map((q) => {
            const questionId = q.id || q._id;
            const createdTime = q.createdAt || q.created_at;
            const similarQuestionsList = q.similarQuestions || q.similar_questions || [];
            
            return (
              <div key={questionId} className="bg-white rounded-2xl shadow-sm border border-slate-150 overflow-hidden hover:shadow-md hover:border-indigo-150 transition duration-200">
                <div className="p-6">
                  <div className="flex flex-col sm:flex-row justify-between items-start mb-4 gap-4">
                    <h3 className="text-lg font-bold text-slate-900 leading-snug">{q.question}</h3>
                    <div className="flex flex-row sm:flex-col items-center sm:items-end gap-2 shrink-0">
                      <span className="bg-indigo-50/80 text-indigo-700 px-3 py-1 rounded-full text-xs font-bold border border-indigo-100 uppercase tracking-wider flex items-center">
                        <Tag className="w-3.5 h-3.5 mr-1.5" /> {q.topic}
                      </span>
                      {q.confidence !== undefined && q.confidence !== null && (
                        <span className="bg-green-50/80 text-green-700 border border-green-100 px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider">
                          {q.confidence}% Confidence
                        </span>
                      )}
                    </div>
                  </div>
                  
                  <div className="flex items-center text-xs font-bold text-slate-400 mb-5 border-b border-slate-50 pb-3">
                    <Calendar className="w-3.5 h-3.5 mr-1.5" />
                    {createdTime ? new Date(createdTime).toLocaleString() : 'N/A'}
                  </div>

                  <div>
                    <h4 className="text-sm font-bold text-slate-700 mb-3 flex items-center">
                      <Search className="w-4 h-4 mr-1.5 text-indigo-600" /> Similar Questions Found:
                    </h4>
                    {similarQuestionsList.length > 0 ? (
                      <div className="grid gap-2">
                        {similarQuestionsList.slice(0, 5).map((sq, idx) => {
                          const score = sq.similarityScore !== undefined ? sq.similarityScore : sq.similarity_score;
                          return (
                            <div key={idx} className="text-sm text-slate-700 flex justify-between items-center bg-slate-50 px-4 py-3 rounded-xl border border-slate-150 hover:bg-slate-100/50 hover:border-slate-200 transition duration-150">
                              <span className="font-semibold truncate pr-4 text-slate-800">{sq.question}</span>
                              <span className="text-indigo-600 font-extrabold whitespace-nowrap bg-indigo-50 border border-indigo-100 px-2 py-0.5 rounded-full text-xs">
                                {(score * 100).toFixed(0)}% Match
                              </span>
                            </div>
                          );
                        })}
                      </div>
                    ) : (
                      <p className="text-xs text-slate-400 font-semibold italic">No similar questions were found at the time.</p>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="bg-white rounded-2xl shadow-sm border border-slate-150 p-16 text-center">
          <HelpCircle className="mx-auto h-16 w-16 text-slate-350 mb-4" />
          <h3 className="text-xl font-bold text-slate-800 mb-1">No questions found</h3>
          <p className="text-slate-500 max-w-md mx-auto font-medium">
            {searchQuery ? (
              filterTopic === 'All' 
                ? `No questions matched "${searchQuery}".`
                : `No questions under "${filterTopic}" matched "${searchQuery}".`
            ) : (
              filterTopic === 'All' 
                ? "You haven't asked any study questions yet. Head to the 'Ask Question' page to start learning!" 
                : `You haven't asked any questions classified under '${filterTopic}' yet.`
            )}
          </p>
        </div>
      )}
    </div>
  );
};

export default History;
