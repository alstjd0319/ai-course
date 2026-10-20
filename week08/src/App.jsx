import React, { useState } from 'react';
import { calculateParkingFee, formatDuration, formatCurrency } from './parking-logic';

function App() {
  const [entryTime, setEntryTime] = useState('');
  const [exitTime, setExitTime] = useState('');
  const [error, setError] = useState('');
  const [history, setHistory] = useState([]);

  const handleCalculate = () => {
    setError('');
    try {
      const result = calculateParkingFee(entryTime, exitTime);
      
      const newEntry = {
        id: Date.now(),
        entry: entryTime,
        exit: exitTime,
        durationText: formatDuration(result.duration),
        fee: result.fee
      };

      setHistory(prev => [...prev, newEntry]);
      setEntryTime('');
      setExitTime('');
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDelete = (id) => {
    setHistory(prev => prev.filter(item => item.id !== id));
  };

  const totalAmount = history.reduce((sum, item) => sum + item.fee, 0);

  return (
    <div className="container">
      <h1>🅿️ 주차 계산기</h1>
      
      <div className="input-group">
        <label>입차 시각</label>
        <input 
          type="text" 
          value={entryTime} 
          onChange={(e) => setEntryTime(e.target.value)} 
          placeholder="09:00"
        />
      </div>

      <div className="input-group">
        <label>출차 시각</label>
        <input 
          type="text" 
          value={exitTime} 
          onChange={(e) => setExitTime(e.target.value)} 
          placeholder="18:00"
        />
      </div>

      <button onClick={handleCalculate}>계산하기</button>
      
      {error && <div className="error">{error}</div>}

      <div className="summary">
        <h3 className="total-header">
          총 합계: <span>{formatCurrency(totalAmount)}</span>원
        </h3>
        
        <table>
          <thead>
            <tr>
              <th>입/출</th>
              <th>시간</th>
              <th>요금</th>
              <th>관리</th>
            </tr>
          </thead>
          <tbody>
            {history.length === 0 ? (
              <tr>
                <td colSpan="4" style={{ textAlign: 'center', color: '#888' }}>내역이 없습니다.</td>
              </tr>
            ) : (
              history.map((item) => (
                <tr key={item.id}>
                  <td>{item.entry}~{item.exit}</td>
                  <td>{item.durationText}</td>
                  <td>{formatCurrency(item.fee)}원</td>
                  <td>
                    <button className="delete-btn" onClick={() => handleDelete(item.id)}>삭제</button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;
