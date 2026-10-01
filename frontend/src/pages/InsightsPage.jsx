import { TrendingUp, Activity, Clock, PieChart } from 'lucide-react'
import { insightsData } from '../data/demoData'

const InsightsPage = () => {
  return (
    <div className="min-h-screen bg-slate-50 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl font-bold text-slate-900">Insights</h1>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          {/* Study Time */}
          <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
            <div className="flex items-center justify-between mb-3">
              <TrendingUp size={20} className="text-slate-400" />
              <span className="text-sm font-medium text-slate-600">Study Time</span>
            </div>
            <div className="flex items-baseline gap-2">
              <p className="text-2xl font-bold text-slate-900">{insightsData.studyTime.totalHours}h</p>
              <p className="text-sm text-slate-500">
                {insightsData.studyTime.changePercent >= 0 ? '+' : ''}{insightsData.studyTime.changePercent}% vs last month
              </p>
            </div>
          </div>

          {/* Sessions Completed */}
          <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
            <div className="flex items-center justify-between mb-3">
              <Activity size={20} className="text-slate-400" />
              <span className="text-sm font-medium text-slate-600">Sessions Completed</span>
            </div>
            <div className="flex items-baseline gap-2">
              <p className="text-2xl font-bold text-slate-900">{insightsData.sessionsCompleted.total}</p>
              <p className="text-sm text-slate-500">
                {insightsData.sessionsCompleted.thisWeek} this week
              </p>
            </div>
          </div>

          {/* Avg Session Duration */}
          <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
            <div className="flex items-center justify-between mb-3">
              <Clock size={20} className="text-slate-400" />
              <span className="text-sm font-medium text-slate-600">Avg Session Duration</span>
            </div>
            <div className="flex items-baseline gap-2">
              <p className="text-2xl font-bold text-slate-900">{insightsData.avgDuration.overall} min</p>
              <p className="text-sm text-slate-500">
                {insightsData.avgDuration.thisWeek} min this week
              </p>
            </div>
          </div>

          {/* Subject Distribution */}
          <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
            <div className="flex items-center justify-between mb-3">
              <PieChart size={20} className="text-slate-400" />
              <span className="text-sm font-medium text-slate-600">Subject Distribution</span>
            </div>
            <div className="space-y-2">
              {insightsData.subjectDistribution.map((item) => (
                <div key={item.subject} className="flex items-center justify-between text-sm">
                  <span>{item.subject}</span>
                  <span>{item.hours}h</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Fatigue Trend */}
          <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
            <h2 className="text-xl font-semibold text-slate-900 mb-4">Fatigue Trend</h2>
            <div className="h-64">
              <div className="relative">
                {/* Simple line chart using divs */}
                <div className="absolute inset-0 pointer-events-none">
                  <div className="flex h-full items-end justify-between space-x-1">
                    {insightsData.fatigueTrend.map((point, index) => (
                      <div key={index} className="relative">
                        <div className={`w-2 bg-${point.level < 40 ? 'green-500' : point.level < 50 ? 'yellow-500' : 'red-500'}`}
                          style={{ height: `${(point.level / 100) * 100}%` }}
                        />
                        <div className="absolute bottom-full mb-1 text-xs text-slate-500">
                          {insightsData.fatigueTrend[index].day}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="absolute inset-0 pointer-events-none flex items-end justify-between text-xs text-slate-400">
                  <div className="mb-2">0</div>
                  <div className="mb-2">25</div>
                  <div className="mb-2">50</div>
                  <div className="mb-2">75</div>
                  <div className="mb-2">100</div>
                </div>
              </div>
            </div>
          </div>

          {/* Sessions by Subject */}
          <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
            <h2 className="text-xl font-semibold text-slate-900 mb-4">Study Time by Subject</h2>
            <div className="space-y-4">
              {insightsData.subjectDistribution.map((item) => (
                <div key={item.subject} className="flex items-center gap-3">
                  <div className="w-20 h-4 bg-slate-200 rounded-full relative">
                    <div
                      className={`h-4 bg-${item.color} rounded-full`}
                      style={{ width: `${(item.hours / Math.max(...insightsData.subjectDistribution.map(d => d.hours))) * 100}%` }}
                    />
                  </div>
                  <div className="flex-1">
                    <p className="text-sm font-medium text-slate-900">{item.subject}</p>
                    <p className="text-xs text-slate-500">{item.hours} hours</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Additional Insights */}
        <div className="mt-8">
          <h2 className="text-xl font-semibold text-slate-900 mb-6">Study Patterns</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
              <h3 className="text-sm font-medium text-slate-600">Best Study Time</h3>
              <p className="text-lg font-bold text-slate-900">7:00 PM - 9:00 PM</p>
              <p className="text-xs text-slate-500 mt-2">Lowest average fatigue detected</p>
            </div>
            <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
              <h3 className="text-sm font-medium text-slate-600">Focus Streak</h3>
              <p className="text-2xl font-bold text-slate-900">{insightsData.sessionsCompleted.streak} days</p>
              <p className="text-xs text-slate-500 mt-2">Consecutive days with study sessions</p>
            </div>
            <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
              <h3 className="text-sm font-medium text-slate-600">Weekly Goal</h3>
              <p className="text-2xl font-bold text-slate-900">{insightsData.sessionsCompleted.thisWeek}/7 sessions</p>
              <p className="text-xs text-slate-500 mt-2">Target: 7 sessions per week</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default InsightsPage