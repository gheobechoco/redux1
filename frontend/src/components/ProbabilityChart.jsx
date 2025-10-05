import { useEffect, useRef } from 'react'
import Chart from 'chart.js/auto'

export default function ProbabilityChart({ result }) {
  const ref = useRef(null)
  useEffect(() => {
    if (!result || !ref.current) return
    const ctx = ref.current.getContext('2d')
    const chart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Mean', 'Median', 'P90'],
        datasets: [{
          label: 'Precip (mm)',
          data: [result.stats.mean_precip_mm, result.stats.median_precip_mm, result.stats.percentile_90_precip_mm],
          backgroundColor: '#6366f1'
        }]
      },
      options: { responsive: true, maintainAspectRatio: false }
    })
    return () => chart.destroy()
  }, [result])

  return (
    <div className="bg-white rounded shadow p-4 h-60">
      <h2 className="font-semibold mb-2">Historical Stats</h2>
      <canvas ref={ref} />
    </div>
  )
}
