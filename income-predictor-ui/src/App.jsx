import { useState } from 'react'
function App() {
  const [form, setForm] = useState({ age: 35, education_num: 13, hours_per_week: 40, capital_gain: 0, capital_loss: 0 })
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const handleChange = e => setForm({ ...form, [e.target.name]: Number(e.target.value) })
  const predict = async () => {
    setLoading(true)
    try {
      const res = await fetch('http://127.0.0.1:8002/predict', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form) })
      const data = await res.json()
      setResult(data.prediction)
    } catch (e) { setResult('Error: Cannot connect to API') }
    setLoading(false)
  }
  return (
    <div style={{ maxWidth:500, margin:'50px auto', fontFamily:'Arial', padding:30, background:'#0d1117', color:'white', borderRadius:12, boxShadow:'0 4px 20px rgba(0,0,0,0.5)' }}>
      <h1 style={{ color:'#2196F3', textAlign:'center', marginBottom:5 }}>Income Predictor</h1>
      <p style={{ textAlign:'center', color:'#8b949e', marginBottom:25 }}>MLOps Assignment - ReactJS Frontend</p>
      {['age','education_num','hours_per_week','capital_gain','capital_loss'].map(field => (
        <div key={field} style={{ marginBottom:15 }}>
          <label style={{ display:'block', marginBottom:5, color:'#58a6ff' }}>{field.replace(/_/g,' ').replace(/\b\w/g,c=>c.toUpperCase())}</label>
          <input type="number" name={field} value={form[field]} onChange={handleChange} style={{ width:'100%', padding:10, borderRadius:6, border:'1px solid #30363d', background:'#161b22', color:'white', fontSize:16, boxSizing:'border-box' }} />
        </div>
      ))}
      <button onClick={predict} style={{ width:'100%', padding:14, background:'#2196F3', color:'white', border:'none', borderRadius:6, fontSize:18, cursor:'pointer', marginTop:10 }}>
        {loading ? 'Predicting...' : 'Predict Income'}
      </button>
      {result && <div style={{ marginTop:25, padding:20, borderRadius:8, background: result.includes('>50K') ? '#1a3a1a' : '#3a2a0a', textAlign:'center' }}>
        <h2 style={{ color: result.includes('>50K') ? '#4caf50' : '#ff9800', margin:0 }}>Result: {result}</h2>
      </div>}
    </div>
  )
}
export default App