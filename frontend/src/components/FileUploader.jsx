import { useState } from 'react'
import { useDropzone } from 'react-dropzone'
import axios from 'axios'

const FileUploader = () => {
  const [file, setFile] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const onDrop = (acceptedFiles) => {
    if (acceptedFiles && acceptedFiles.length > 0) {
      setFile(acceptedFiles[0])
      setResult(null)
      setError(null)
    }
  }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png'],
      'video/*': ['.mp4', '.avi'],
      'application/pdf': ['.pdf']
    },
    maxSize: 100 * 1024 * 1024, // 100MB max size
    multiple: false
  })

  const uploadFile = async () => {
    if (!file) return

    setIsLoading(true)
    setError(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await axios.post('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      setResult(response.data)
    } catch (error) {
      console.error('Error uploading file:', error)
      setError(error.response?.data?.detail || 'Error uploading file')
    } finally {
      setIsLoading(false)
    }
  }

  const getFileTypeIcon = () => {
    if (!file) return null
    if (file.type.startsWith('image/')) return '🖼️'
    if (file.type.startsWith('video/')) return '🎬'
    if (file.type === 'application/pdf') return '📄'
    return '📁'
  }

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer ${
          isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-blue-400'
        }`}
      >
        <input {...getInputProps()} />
        {isDragActive ? (
          <p className="text-blue-500">Drop the file here...</p>
        ) : (
          <>
            <p className="text-gray-500">
              Drag and drop a file here, or click to select a file
            </p>
            <p className="text-sm text-gray-400 mt-2">
              Supported formats: Images (JPG, PNG), Videos (MP4, AVI), Documents (PDF)
            </p>
          </>
        )}
      </div>

      {file && (
        <div className="mt-4 p-4 bg-white rounded-lg shadow">
          <div className="flex items-center">
            <span className="text-2xl mr-2">{getFileTypeIcon()}</span>
            <div>
              <p className="font-semibold">{file.name}</p>
              <p className="text-sm text-gray-500">
                {(file.size / 1024 / 1024).toFixed(2)} MB
              </p>
            </div>
          </div>
          <button
            onClick={uploadFile}
            disabled={isLoading}
            className={`mt-4 w-full py-2 px-4 rounded-md text-white font-medium ${
              isLoading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700'
            }`}
          >
            {isLoading ? 'Processing...' : 'Upload and Detect'}
          </button>
        </div>
      )}

      {error && (
        <div className="mt-4 p-4 bg-red-50 text-red-700 rounded-lg">
          <p className="font-semibold">Error</p>
          <p>{error}</p>
        </div>
      )}

      {result && (
        <div className="mt-4 p-4 bg-white rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-2">Detection Result</h3>
          <div className={`p-3 rounded-md ${result.result ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`}>
            <p className="font-bold text-lg">
              {result.message}
            </p>
          </div>

          {/* Display detection details */}
          {result.result && (
            <div className="mt-4">
              <h4 className="font-semibold mb-2">Details:</h4>
              
              {/* For Image */}
              {result.result_image_url && (
                <div className="mt-2">
                  <p className="text-sm text-gray-500 mb-1">Detected image:</p>
                  <img 
                    src={result.result_image_url} 
                    alt="Detection result" 
                    className="w-full rounded-md shadow border border-gray-200" 
                  />
                </div>
              )}
              
              {/* For Video */}
              {result.detections && result.detections.length > 0 && result.detections[0].frame_url && (
                <div className="mt-2">
                  <p className="text-sm text-gray-500 mb-1">Detected in {result.detections.length} frames:</p>
                  <div className="grid grid-cols-2 gap-2 mt-1">
                    {result.detections.slice(0, 4).map((detection, index) => (
                      <div key={index} className="relative">
                        <img 
                          src={detection.frame_url} 
                          alt={`Frame at ${detection.time.toFixed(2)}s`} 
                          className="w-full rounded-md shadow border border-gray-200" 
                        />
                        <span className="absolute bottom-1 right-1 bg-black bg-opacity-70 text-white text-xs px-1 rounded">
                          {detection.time.toFixed(2)}s
                        </span>
                      </div>
                    ))}
                  </div>
                  {result.detections.length > 4 && (
                    <p className="text-sm text-gray-500 mt-1">
                      And {result.detections.length - 4} more frames...
                    </p>
                  )}
                </div>
              )}
              
              {/* For PDF */}
              {result.detections && result.detections.length > 0 && result.detections[0].page_url && (
                <div className="mt-2">
                  <p className="text-sm text-gray-500 mb-1">Detected in {result.detections.length} pages:</p>
                  <div className="grid grid-cols-2 gap-2 mt-1">
                    {result.detections.slice(0, 4).map((detection, index) => (
                      <div key={index} className="relative">
                        <img 
                          src={detection.page_url} 
                          alt={`Page ${detection.page_number}`} 
                          className="w-full rounded-md shadow border border-gray-200" 
                        />
                        <span className="absolute bottom-1 right-1 bg-black bg-opacity-70 text-white text-xs px-1 rounded">
                          Page {detection.page_number}
                        </span>
                      </div>
                    ))}
                  </div>
                  {result.detections.length > 4 && (
                    <p className="text-sm text-gray-500 mt-1">
                      And {result.detections.length - 4} more pages...
                    </p>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default FileUploader
