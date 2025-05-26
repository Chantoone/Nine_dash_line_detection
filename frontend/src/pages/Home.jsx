import FileUploader from '../components/FileUploader'

const Home = () => {
  return (
    <div>
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">Nine Dash Line Detection System</h1>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Upload an image, video, or PDF document to automatically detect the presence of the "Nine Dash Line" (also known as "đường lưỡi bò").
        </p>
      </div>
      
      <FileUploader />
      
      <div className="mt-12 max-w-2xl mx-auto bg-blue-50 p-4 rounded-lg text-blue-800">
        <h3 className="font-semibold text-lg mb-2">How it works</h3>
        <p className="mb-2">This system uses a trained Faster R-CNN model to detect the "Nine Dash Line" in your uploaded files:</p>
        <ul className="list-disc list-inside space-y-1 pl-2">
          <li>For images: Direct detection on the image</li>
          <li>For videos: Analysis of key frames extracted from the video</li>
          <li>For PDFs: Analysis of each page converted to an image</li>
        </ul>
      </div>
    </div>
  )
}

export default Home
