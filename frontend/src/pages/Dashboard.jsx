import StatisticsCard from '../components/StatisticsCard'

const Dashboard = () => {
  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">System Dashboard</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <StatisticsCard />
        
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4">System Information</h3>
          
          <div className="space-y-4">
            <div>
              <h4 className="font-medium text-gray-700">Model Details</h4>
              <p className="text-gray-600">Faster R-CNN with ResNet-50 backbone</p>
              <p className="text-sm text-gray-500">Trained on 1000+ images containing the Nine Dash Line pattern</p>
            </div>
            
            <div>
              <h4 className="font-medium text-gray-700">Performance</h4>
              <div className="flex items-center mt-1">
                <div className="flex-1">
                  <p className="text-sm text-gray-600">Precision</p>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div className="bg-green-600 h-2 rounded-full" style={{ width: '92%' }}></div>
                  </div>
                  <p className="text-right text-xs text-gray-500">92%</p>
                </div>
                <div className="w-8"></div>
                <div className="flex-1">
                  <p className="text-sm text-gray-600">Recall</p>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div className="bg-blue-600 h-2 rounded-full" style={{ width: '88%' }}></div>
                  </div>
                  <p className="text-right text-xs text-gray-500">88%</p>
                </div>
              </div>
            </div>
            
            <div>
              <h4 className="font-medium text-gray-700">System Status</h4>
              <div className="flex items-center">
                <span className="h-3 w-3 bg-green-500 rounded-full mr-2"></span>
                <span className="text-green-700">Operational</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
