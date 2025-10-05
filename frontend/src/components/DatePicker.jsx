export default function DatePicker({ value, onChange }) {
  const onMonth = (e) => onChange({ ...value, month: Number(e.target.value) })
  const onDay = (e) => onChange({ ...value, day: Number(e.target.value) })

  return (
    <div className="bg-white rounded shadow p-4 flex gap-4 items-end">
      <div>
        <label className="block text-sm text-slate-600">Month</label>
        <select value={value.month} onChange={onMonth} className="border rounded p-2">
          {Array.from({ length: 12 }, (_, i) => i + 1).map(m => (
            <option key={m} value={m}>{m}</option>
          ))}
        </select>
      </div>
      <div>
        <label className="block text-sm text-slate-600">Day</label>
        <select value={value.day} onChange={onDay} className="border rounded p-2">
          {Array.from({ length: 31 }, (_, i) => i + 1).map(d => (
            <option key={d} value={d}>{d}</option>
          ))}
        </select>
      </div>
    </div>
  )
}
