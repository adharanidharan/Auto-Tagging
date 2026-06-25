import { useState, useEffect } from 'react';
import api from '../services/api';
import { 
  Send, Tag, Lightbulb, CheckCircle2, AlertCircle, ThumbsUp, ThumbsDown, 
  Sparkles, ShieldCheck, Compass, HelpCircle
} from 'lucide-react';

const AskQuestion = () => {
  const [question, setQuestion] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [currentModel, setCurrentModel] = useState('MiniLM Embedding Model');

  // Feedback states
  const [feedbackRating, setFeedbackRating] = useState(null); // 'good' or 'wrong'
  const [showFeedbackForm, setShowFeedbackForm] = useState(false);
  const [feedbackTopic, setFeedbackTopic] = useState('');
  const [feedbackComment, setFeedbackComment] = useState('');
  const [feedbackSubmitted, setFeedbackSubmitted] = useState(false);
  const [feedbackSubmitting, setFeedbackSubmitting] = useState(false);
  const [allTopics, setAllTopics] = useState([]);

  // Sync current model choice from localStorage
  const updateModelFromStorage = () => {
    const savedModel = localStorage.getItem('selectedModel') || 'MiniLM Embedding Model';
    setCurrentModel(savedModel);
  };

  useEffect(() => {
    updateModelFromStorage();
    window.addEventListener('modelChanged', updateModelFromStorage);
    
    // Fetch all active topics for correction dropdown
    const fetchTopics = async () => {
      try {
        const response = await api.get('/topics');
        setAllTopics(response.data);
      } catch (err) {
        console.error('Failed to fetch topics for correction dropdown:', err);
      }
    };
    fetchTopics();

    return () => {
      window.removeEventListener('modelChanged', updateModelFromStorage);
    };
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (question.trim().length < 5) {
      setError('Question must be at least 5 characters long.');
      return;
    }
    
    setLoading(true);
    setError('');
    setResult(null);

    // Reset feedback states
    setFeedbackRating(null);
    setShowFeedbackForm(false);
    setFeedbackTopic('');
    setFeedbackComment('');
    setFeedbackSubmitted(false);

    try {
      const selectedModel = localStorage.getItem('selectedModel') || 'MiniLM Embedding Model';
      const response = await api.post('/questions', { 
        question: question.trim(), 
        model: selectedModel 
      });
      setResult(response.data);
      setQuestion('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to submit question. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleFeedbackSubmit = async (rating, correctTopic) => {
    if (!result) return;
    setFeedbackSubmitting(true);
    setError('');

    try {
      const questionId = result._id || result.id;
      await api.post('/feedback', {
        questionId: questionId,
        predictedTopic: result.topic,
        correctTopic: correctTopic,
        rating: rating,
        comment: feedbackComment.trim() || undefined
      });
      setFeedbackSubmitted(true);
      setShowFeedbackForm(false);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to submit feedback.');
    } finally {
      setFeedbackSubmitting(false);
    }
  };

  const similarQuestionsList = result 
    ? (result.similarQuestions || result.similar_questions || []) 
    : [];

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in">
      {/* Title */}
      <div className="mb-8">
        <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
          <Compass className="h-8 w-8 text-indigo-600" />
          Ask a New Question
        </h1>
        <p className="text-slate-500 mt-1 font-medium">
          Get immediate topic categorization and find matching questions from the repository.
        </p>
      </div>
      
      {/* Form Container */}
      <div className="bg-white rounded-2xl shadow-xl shadow-slate-100/50 border border-slate-150 p-6 mb-8 hover:shadow-xl hover:border-slate-200 transition duration-350">
        <form onSubmit={handleSubmit}>
          <div className="mb-5">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 mb-3">
              <label htmlFor="question" className="block text-sm font-bold text-slate-700">
                What do you want to learn today?
              </label>
              <span className="inline-flex items-center text-xs font-bold text-indigo-700 bg-indigo-50/80 px-3 py-1 rounded-full border border-indigo-100">
                Active Model: {currentModel}
              </span>
            </div>
            <textarea
              id="question"
              rows={4}
              className="w-full border-slate-250 rounded-xl shadow-inner focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 p-3 border outline-none text-slate-800 transition placeholder-slate-400 text-sm"
              placeholder="E.g., What is Newton's second law of motion?"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              disabled={loading}
            />
          </div>
          
          {error && (
            <div className="mb-5 flex items-start gap-2 text-sm text-red-650 bg-red-50 p-4 rounded-xl border border-red-100 animate-fade-in-up">
              <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
              <span>{error}</span>
            </div>
          )}

          <div className="flex justify-end">
            <button
              type="submit"
              disabled={loading || !question.trim()}
              className="inline-flex items-center px-6 py-2.5 border border-transparent text-sm font-bold rounded-xl shadow-md text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 transition duration-150 cursor-pointer"
            >
              {loading ? (
                <>
                  <div className="animate-spin -ml-1 mr-2 h-4 w-4 text-white border-2 border-b-transparent rounded-full"></div>
                  AI Analyzing...
                </>
              ) : (
                <>
                  <Send className="-ml-1 mr-2 h-4 w-4" />
                  Ask Question
                </>
              )}
            </button>
          </div>
        </form>
      </div>

      {/* Results Container */}
      {result && (
        <div className="animate-fade-in-up space-y-8">
          <div className="bg-gradient-to-br from-indigo-50/60 to-purple-50/40 border border-indigo-100 rounded-2xl p-6 shadow-sm">
            <div className="flex items-center mb-5 border-b border-indigo-100/50 pb-3">
              <Sparkles className="h-5 w-5 text-indigo-600 mr-2 animate-pulse" />
              <h2 className="text-lg font-bold text-indigo-950">AI Classification Complete!</h2>
            </div>
            
            <div className="flex flex-col sm:flex-row gap-4 mb-6">
              <div className="bg-white px-5 py-4 rounded-xl shadow-sm border border-indigo-50 flex-1">
                <p className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1.5 flex items-center gap-1">
                  <Tag className="w-3.5 h-3.5 text-indigo-500" /> Auto-Detected Topic
                </p>
                <p className="font-black text-indigo-700 text-xl capitalize">{result.topic}</p>
              </div>
              {result.confidence !== undefined && result.confidence !== null && (
                <div className="bg-white px-5 py-4 rounded-xl shadow-sm border border-indigo-50 flex-1">
                  <p className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1.5 flex items-center gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5 text-green-500" /> Classification Confidence
                  </p>
                  <p className="font-black text-green-700 text-xl">{result.confidence}%</p>
                </div>
              )}
            </div>

            {/* User Feedback Widget */}
            <div className="border-t border-indigo-100/50 pt-4">
              {!feedbackSubmitted ? (
                <div>
                  <p className="text-xs font-bold text-indigo-950 mb-3 flex items-center gap-1.5">
                    <CheckCircle2 className="w-4 h-4 text-indigo-600" />
                    Was this topic classification correct?
                  </p>
                  <div className="flex gap-2.5 items-center">
                    <button
                      onClick={() => handleFeedbackSubmit('good', result.topic)}
                      disabled={feedbackSubmitting}
                      className="inline-flex items-center px-4 py-2 bg-white border border-slate-200 text-green-700 hover:text-green-800 hover:border-green-300 text-xs font-bold rounded-lg hover:bg-green-50 transition shadow-sm cursor-pointer"
                    >
                      <ThumbsUp className="w-3.5 h-3.5 mr-1.5 text-green-500" /> Yes, correct
                    </button>
                    <button
                      onClick={() => {
                        setFeedbackRating('wrong');
                        setShowFeedbackForm(true);
                      }}
                      disabled={feedbackSubmitting}
                      className="inline-flex items-center px-4 py-2 bg-white border border-slate-200 text-red-700 hover:text-red-800 hover:border-red-300 text-xs font-bold rounded-lg hover:bg-red-50 transition shadow-sm cursor-pointer"
                    >
                      <ThumbsDown className="w-3.5 h-3.5 mr-1.5 text-red-500" /> No, incorrect
                    </button>
                  </div>

                  {showFeedbackForm && (
                    <div className="mt-5 bg-white border border-slate-150 rounded-xl p-5 shadow-sm animate-fade-in-up">
                      <div className="mb-4">
                        <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">
                          Select Correct Topic
                        </label>
                        <select
                          value={feedbackTopic}
                          onChange={(e) => setFeedbackTopic(e.target.value)}
                          className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-sm text-slate-800 focus:bg-white focus:border-indigo-500 outline-none transition cursor-pointer"
                        >
                          <option value="">-- Choose correct topic --</option>
                          {allTopics.map((t, idx) => (
                            <option key={idx} value={t}>{t}</option>
                          ))}
                        </select>
                      </div>

                      <div className="mb-4">
                        <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">
                          Comments (Optional)
                        </label>
                        <textarea
                          rows={2}
                          value={feedbackComment}
                          onChange={(e) => setFeedbackComment(e.target.value)}
                          placeholder="Explain why this topic is incorrect or suggest improvements..."
                          className="w-full border border-slate-200 rounded-lg p-2.5 text-sm text-slate-800 focus:border-indigo-500 outline-none transition"
                        />
                      </div>

                      <div className="flex justify-end gap-2.5">
                        <button
                          type="button"
                          onClick={() => {
                            setShowFeedbackForm(false);
                            setFeedbackRating(null);
                          }}
                          className="px-4 py-2 border border-slate-200 text-xs font-bold text-slate-600 bg-white rounded-lg hover:bg-slate-50 transition cursor-pointer"
                        >
                          Cancel
                        </button>
                        <button
                          type="button"
                          onClick={() => handleFeedbackSubmit('wrong', feedbackTopic)}
                          disabled={feedbackSubmitting || !feedbackTopic}
                          className="px-5 py-2 border border-transparent text-xs font-bold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 disabled:opacity-50 transition flex items-center justify-center cursor-pointer"
                        >
                          {feedbackSubmitting ? 'Submitting...' : 'Submit Feedback'}
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div className="flex items-center gap-2 text-green-700 bg-white/80 p-4 rounded-xl border border-green-200/80 shadow-sm animate-fade-in-up">
                  <CheckCircle2 className="w-5 h-5 text-green-500 flex-shrink-0" />
                  <span className="text-xs font-bold">Thank you! Your feedback has been registered to help optimize our AI models.</span>
                </div>
              )}
            </div>

          </div>

          <div>
            <h3 className="text-xl font-bold text-slate-900 mb-5 flex items-center">
              <Lightbulb className="h-5 w-5 mr-2 text-yellow-500 animate-pulse" />
              Similar Existing Questions
            </h3>
            
            {similarQuestionsList.length > 0 ? (
              <div className="space-y-4">
                {similarQuestionsList.map((sq, index) => {
                  const score = sq.similarityScore !== undefined ? sq.similarityScore : sq.similarity_score;
                  return (
                    <div key={index} className="bg-white rounded-xl shadow-sm border border-slate-150 p-5 hover:shadow-md hover:border-indigo-150 transition duration-150">
                      <p className="text-slate-800 font-semibold mb-3">{sq.question}</p>
                      <div className="flex items-center justify-between text-xs pt-3 border-t border-slate-50">
                        <span className="bg-slate-50 text-slate-600 px-2.5 py-1 rounded-md font-bold border border-slate-200/60 uppercase tracking-wider">
                          {sq.topic}
                        </span>
                        <span className="text-slate-500 font-medium">
                          Similarity Match: <span className="font-extrabold text-indigo-600 bg-indigo-50/50 border border-indigo-100 px-2 py-0.5 rounded ml-1">{(score * 100).toFixed(1)}%</span>
                        </span>
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className="bg-white rounded-xl shadow-sm border border-slate-150 p-8 text-center text-slate-500 font-semibold italic">
                This is a very unique question! No highly similar questions found in the database.
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default AskQuestion;
