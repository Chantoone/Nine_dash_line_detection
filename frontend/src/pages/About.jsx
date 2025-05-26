const About = () => {
  return (
    <div className="max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">About the Nine Dash Line Detection System</h1>
      
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">What is the "Nine Dash Line"?</h2>
        <p className="text-gray-700 mb-4">
          The "Nine Dash Line" (also known as "đường lưỡi bò" in Vietnamese) is a demarcation line used by China for its claims of a major part of the South China Sea. 
          The presence of this line in maps, documents, or media can be politically sensitive and may be subject to regulation in certain contexts.
        </p>
        <p className="text-gray-700">
          This detection system uses artificial intelligence to automatically identify this pattern in various types of media, helping users 
          ensure compliance with relevant guidelines and regulations.
        </p>
      </div>
      
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">How Our System Works</h2>
        
        <div className="space-y-4">
          <div>
            <h3 className="font-medium text-gray-800">AI Model</h3>
            <p className="text-gray-700">
              We use a Faster R-CNN deep learning model with a VGG-16 backbone, specifically trained to recognize the Nine Dash Line pattern 
              in various forms, colors, and contexts.
            </p>
          </div>
          
          <div>
            <h3 className="font-medium text-gray-800">Supported File Types</h3>
            <ul className="list-disc list-inside text-gray-700 pl-4">
              <li>Images: JPG, JPEG, PNG</li>
              <li>Videos: MP4, AVI</li>
              <li>Documents: PDF</li>
            </ul>
          </div>
          
          <div>
            <h3 className="font-medium text-gray-800">Processing Pipeline</h3>
            <ol className="list-decimal list-inside text-gray-700 pl-4 space-y-1">
              <li>File upload and validation</li>
              <li>Preprocessing (resizing, frame extraction for videos, page extraction for PDFs)</li>
              <li>AI model detection</li>
              <li>Result visualization with bounding boxes around detected patterns</li>
              <li>Result delivery to the user</li>
            </ol>
          </div>
        </div>
      </div>
      
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Technical Implementation</h2>
        <div className="space-y-4">
          <div>
            <h3 className="font-medium text-gray-800">Backend</h3>
            <p className="text-gray-700">
              Our system is built with Python using FastAPI, providing a high-performance REST API for file uploads and processing.
            </p>
          </div>
          
          <div>
            <h3 className="font-medium text-gray-800">Frontend</h3>
            <p className="text-gray-700">
              The user interface is built with React and styled with Tailwind CSS, providing a responsive and intuitive experience.
            </p>
          </div>
          
          <div>
            <h3 className="font-medium text-gray-800">Specialized Processing</h3>
            <ul className="list-disc list-inside text-gray-700 pl-4">
              <li>Video processing: OpenCV for frame extraction and processing</li>
              <li>PDF processing: pdf2image for converting PDF pages to images</li>
              <li>Image visualization: PIL and OpenCV for annotating detection results</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default About
