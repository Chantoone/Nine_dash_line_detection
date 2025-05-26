import { useState, useEffect } from 'react'
import axios from 'axios'

const StatisticsCard = () => {
  const [statistics, setStatistics] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchStatistics = async () => {
      try {
        const response = await axios.get('/api/statistics')
        setStatistics(response.data)
        setLoading(false)
      } catch (err) {
        console.error('Error fetching statistics:', err)
        setError('Failed to load statistics')
        setLoading(false)
      }
    }

    fetchStatistics()
  }, [])

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow p-6 animate-pulse">
        <div className="h-4 bg-gray-200 rounded w-1/2 mb-4"></div>
        <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
        <div className="h-4 bg-gray-200 rounded w-1/4"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-50 text-red-700 rounded-lg shadow p-6">
        <p className="font-semibold">Error</p>
        <p>{error}</p>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold mb-4">System Statistics</h3>
      
      <div className="grid grid-cols-2 gap-4 mb-4">
        <div className="bg-blue-50 p-4 rounded-md">
          <p className="text-sm text-blue-700 font-medium">Images Processed</p>
          <p className="text-2xl font-bold text-blue-900">{statistics.total_processed.images}</p>
        </div>
        
        <div className="bg-green-50 p-4 rounded-md">
          <p className="text-sm text-green-700 font-medium">Video Frames</p>
          <p className="text-2xl font-bold text-green-900">{statistics.total_processed.video_frames}</p>
        </div>
        
        <div className="bg-purple-50 p-4 rounded-md">
          <p className="text-sm text-purple-700 font-medium">PDF Pages</p>
          <p className="text-2xl font-bold text-purple-900">{statistics.total_processed.pdf_pages}</p>
        </div>
        
        <div className="bg-red-50 p-4 rounded-md">
          <p className="text-sm text-red-700 font-medium">Total Detections</p>
          <p className="text-2xl font-bold text-red-900">{statistics.total_detections}</p>
        </div>
      </div>
      
      <p className="text-sm text-gray-500">Last updated: {new Date().toLocaleString()}</p>
    </div>
  )
}

export default StatisticsCard
