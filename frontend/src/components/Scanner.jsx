// src/components/Scanner.jsx
import React, { useState } from 'react';
import axios from 'axios';

const Scanner = () => {
  const [url, setUrl] = useState('');
  const [scanning, setScanning] = useState(false);
  const [results, setResults] = useState(null);
  const [scanHistory, setScanHistory] = useState([]);
  const [error, setError] = useState(null);
    //try 1
    const [filters, setFilters] = useState({
  riskLevel: 'all', // 'all', 'malicious', 'safe'
  tld: 'all',       // 'all', 'com', 'org', 'net', etc.
  dateRange: 'all'  // 'all', 'today', 'week', 'month', 'custom'
});

const [customDateRange, setCustomDateRange] = useState({
  startDate: '',
  endDate: ''
});

// Add this FilterBar component inside your Scanner.jsx, before the results section
const FilterBar = ({ filters, setFilters, customDateRange, setCustomDateRange }) => {
  return (
    <div className="bg-gray-50 rounded-lg p-4 mb-6 border border-gray-200">
      <h3 className="text-lg font-semibold text-gray-800 mb-3">🔍 Filter Results</h3>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* RISK LEVEL FILTER */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Risk Level
          </label>
          <select
            value={filters.riskLevel}
            onChange={(e) => setFilters(prev => ({ ...prev, riskLevel: e.target.value }))}
            className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Results</option>
            <option value="malicious">⚠️ Malicious Only</option>
            <option value="safe">🟢 Safe Only</option>
          </select>
        </div>

        {/* TLD FILTER */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Top Level Domain
          </label>
          <select
            value={filters.tld}
            onChange={(e) => setFilters(prev => ({ ...prev, tld: e.target.value }))}
            className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All TLDs</option>
            <option value="com">.com</option>
            <option value="org">.org</option>
            <option value="net">.net</option>
            <option value="io">.io</option>
            <option value="edu">.edu</option>
            <option value="gov">.gov</option>
            <option value="other">Other TLDs</option>
          </select>
        </div>

        {/* DATE RANGE FILTER */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Date Range
          </label>
          <select
            value={filters.dateRange}
            onChange={(e) => setFilters(prev => ({ ...prev, dateRange: e.target.value }))}
            className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Time</option>
            <option value="today">Today</option>
            <option value="week">Last 7 Days</option>
            <option value="month">Last 30 Days</option>
            <option value="custom">Custom Range</option>
          </select>
        </div>
      </div>

      {/* CUSTOM DATE RANGE INPUTS */}
      {filters.dateRange === 'custom' && (
        <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-3">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Start Date
            </label>
            <input
              type="date"
              value={customDateRange.startDate}
              onChange={(e) => setCustomDateRange(prev => ({ ...prev, startDate: e.target.value }))}
              className="w-full p-2 border border-gray-300 rounded-md"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              End Date
            </label>
            <input
              type="date"
              value={customDateRange.endDate}
              onChange={(e) => setCustomDateRange(prev => ({ ...prev, endDate: e.target.value }))}
              className="w-full p-2 border border-gray-300 rounded-md"
            />
          </div>
        </div>
      )}
    </div>
  );
};

// Filter function to apply all filters to scanHistory
const getFilteredResults = () => {
  return scanHistory.filter(scan => {
    const scanDate = new Date(scan.timestamp || Date.now());
    const now = new Date();

    // Risk Level Filter
    if (filters.riskLevel !== 'all') {
      const isMalicious = scan.filters?.machine_learning?.prediction === 1;
      if (filters.riskLevel === 'malicious' && !isMalicious) return false;
      if (filters.riskLevel === 'safe' && isMalicious) return false;
    }

    // TLD Filter
    if (filters.tld !== 'all') {
      const url = scan.url || '';
      const tld = url.split('.').pop() || '';

      if (filters.tld === 'other') {
        const commonTlds = ['com', 'org', 'net', 'io', 'edu', 'gov'];
        if (commonTlds.includes(tld)) return false;
      } else if (tld !== filters.tld) {
        return false;
      }
    }

    // Date Range Filter
    if (filters.dateRange !== 'all') {
      const timeDiff = now - scanDate;
      const daysDiff = timeDiff / (1000 * 60 * 60 * 24);

      switch (filters.dateRange) {
        case 'today':
          if (daysDiff > 1) return false;
          break;
        case 'week':
          if (daysDiff > 7) return false;
          break;
        case 'month':
          if (daysDiff > 30) return false;
          break;
        case 'custom':
          if (customDateRange.startDate && scanDate < new Date(customDateRange.startDate)) return false;
          if (customDateRange.endDate && scanDate > new Date(customDateRange.endDate)) return false;
          break;
        default:
          break;
      }
    }

    return true;
  });
};
    //end try 1

  const handleScan = async () => {
    if (!url.trim()) {
      setError('Please enter a URL');
      return;
    }

    setScanning(true);
    setError(null);
    setResults(null);

    try {
      const response = await axios.post('http://localhost:8000/scan/url/', {
        url: url
      });

      // ✅ FIX: Better response validation
      if (response.data && response.data.filters) {
        setResults(response.data);
        setScanHistory(prev => [response.data, ...prev.slice(0, 9)]); // Keep last 10 scans
      } else {
        throw new Error('Invalid response structure from server');
      }

    } catch (error) {
      console.error('Scan failed:', error);
      setError(
        error.response?.data?.detail ||
        error.response?.data?.message ||
        error.message ||
        'Scan failed. Please check if backend is running on port 8000.'
      );
    } finally {
      setScanning(false);
    }
  };

  // ✅ FIX: Safe stats calculation
  const stats = {
    total: scanHistory.length,
    malicious: scanHistory.filter(r =>
      r.filters?.machine_learning?.prediction === 1
    ).length,
    safe: scanHistory.filter(r =>
      r.filters?.machine_learning?.prediction === 0
    ).length,
  };

  stats.detectionRate = stats.total > 0 ?
    ((stats.malicious / stats.total) * 100).toFixed(1) : 0;

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
      {/* SCANNER INPUT */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">
          🛡️ URL Security Scanner
        </h2>

        <div className="flex gap-3">
          <input
            type="text"
            value={url}
            onChange={(e) => {
              setUrl(e.target.value);
              setError(null); // Clear error when typing
            }}
            placeholder="Enter URL to scan (e.g., https://example.com)"
            className="flex-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={scanning}
          />

          <button
            onClick={handleScan}
            disabled={scanning || !url.trim()}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition-colors font-semibold"
          >
            {scanning ? '🔄 Scanning...' : '🚀 Scan URL'}
          </button>
        </div>

        {/* ERROR DISPLAY */}
        {error && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-700">❌ {error}</p>
          </div>
        )}
      </div>

      {/* SCAN RESULTS SECTION */}
      {results && !error && (
        <div>
          {/* CENTERED URL SCANNED */}
          <div className="text-center mb-8">
            <h3 className="text-lg font-semibold text-gray-700 mb-2">URL Scanned</h3>
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 max-w-2xl mx-auto">
              <p className="text-blue-800 font-mono text-sm break-all">
                {results.url || 'URL not available'}
              </p>
            </div>
          </div>

          {/* TWO-COLUMN LAYOUT */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* SCAN RESULTS - 2/3 width */}
            <div className="lg:col-span-2">
              <h3 className="text-xl font-bold text-gray-800 mb-4">SCAN RESULTS</h3>

              <div className="grid gap-4">
                {/* ✅ FIX: Changed single_heuristic to simple_heuristic */}
                {results.filters?.simple_heuristic && (
                  <div className={`p-4 rounded-lg border ${
                    results.filters.simple_heuristic.risk_percent > 50
                      ? 'bg-red-50 border-red-200'
                      : 'bg-green-50 border-green-200'
                  }`}>
                    <h4 className="font-bold mb-2">🔍 Simple Heuristic</h4>
                    <p><strong>Risk:</strong> {results.filters.simple_heuristic.risk_percent}%</p>
                    <p><strong>Verdict:</strong> {results.filters.simple_heuristic.result}</p>
                  </div>
                )}

                {/* Advanced Heuristic */}
                {results.filters?.advanced_heuristic && (
                  <div className={`p-4 rounded-lg border ${
                    results.filters.advanced_heuristic.risk >= 50
                      ? 'bg-red-50 border-red-200'
                      : 'bg-green-50 border-green-200'
                  }`}>
                    <h4 className="font-bold mb-2">⚡ Advanced Heuristic</h4>
                    <p><strong>Risk:</strong> {results.filters.advanced_heuristic.risk}%</p>
                    <p><strong>Classification:</strong> {results.filters.advanced_heuristic.classification}</p>
                    {results.filters.advanced_heuristic.reasons?.length > 0 && (
                      <div className="mt-2">
                        <strong>Reasons:</strong>
                        <ul className="list-disc list-inside text-sm">
                          {results.filters.advanced_heuristic.reasons.map((reason, index) => (
                            <li key={index}>{reason}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                )}

                {/* Machine Learning */}
                {results.filters?.machine_learning && (
                  <div className={`p-4 rounded-lg border ${
                    results.filters.machine_learning.prediction === 1
                      ? 'bg-red-50 border-red-200'
                      : results.filters.machine_learning.prediction === 0
                      ? 'bg-green-50 border-green-200'
                      : 'bg-yellow-50 border-yellow-200'
                  }`}>
                    <h4 className="font-bold mb-2">🤖 Machine Learning</h4>
                    <p><strong>Prediction:</strong> {results.filters.machine_learning.classification}</p>
                    <p><strong>Confidence:</strong> {(results.filters.machine_learning.probability * 100).toFixed(1)}%</p>
                    {results.filters.machine_learning.error && (
                      <p className="text-yellow-700 text-sm mt-1">
                        ⚠️ {results.filters.machine_learning.error}
                      </p>
                    )}
                  </div>
                )}
              </div>
            </div>

            {/* QUICK STATS - 1/3 width */}
            <div className="lg:col-span-1">
              <h3 className="text-xl font-bold text-gray-800 mb-4">QUICK STATS</h3>

              <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="font-semibold">Total Scans:</span>
                    <span className="text-blue-600 font-bold">{stats.total}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="font-semibold">Malicious:</span>
                    <span className="text-red-600 font-bold">{stats.malicious}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="font-semibold">Safe:</span>
                    <span className="text-green-600 font-bold">{stats.safe}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="font-semibold">Detection Rate:</span>
                    <span className="text-purple-600 font-bold">{stats.detectionRate}%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Scanner;
