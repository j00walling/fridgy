import React, { useState } from "react";

interface UploadModalProps {
  onClose: () => void;
}

const UploadModal: React.FC<UploadModalProps> = ({ onClose }) => {
  const [file, setFile] = useState<File | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = () => {
    if (file) {
      // Add the upload functionality here, e.g., send to your backend
      console.log("Uploading file:", file);
    }
    onClose(); // Close the modal after uploading
  };

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white p-6 rounded shadow-lg">
        <h2 className="text-lg mb-4">Upload Recipe (PDF)</h2>
        <input type="file" accept="application/pdf" onChange={handleFileChange} />
        <button onClick={handleUpload} className="mt-4 px-4 py-2 bg-blue-500 text-white rounded">
          Upload
        </button>
        <button onClick={onClose} className="mt-2 px-4 py-2 text-gray-500">
          Cancel
        </button>
      </div>
    </div>
  );
};

export default UploadModal;
