"use client";

import { useState, useEffect } from "react";
import axios, { AxiosResponse } from 'axios';
import Search from "@/app/ui/search";
import LoginModal from "@/app/ui/login";
import QueryResponse from "@/app/ui/query-response";
import Sidebar from "@/app/ui/sidebar";
import { Query } from "@/app/types/interfaces";
import { ChevronDownIcon } from "@heroicons/react/24/outline";
import clsx from "clsx";

interface ApiResponse {
  response: {
    id: string;
    choices: Array<{
      finish_reason: string;
      index: number;
      logprobs: any | null;
      message: {
        content: string;
        role: string;
      };
    }>;
    created: number;
    model: string;
    object: string;
    service_tier: string | null;
    system_fingerprint: string | null;
    usage: {
      completion_tokens: number;
      prompt_tokens: number;
      total_tokens: number;
    };
  };
  context: Array<{ role: string; content: string }>;
}

interface User {
  id: number;
  username: string;
}

const ChatInterface = () => {
  const [inputValue, setInputValue] = useState<string>("");
  const [queries, setQueries] = useState<Query[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [context, setContext] = useState<Array<{role: string, content: string}>>([]);
  const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState<User | null>(null);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [isHovered, setIsHovered] = useState<boolean>(false);
  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);

  // File upload states
  const [file, setFile] = useState<File | null>(null);
  const [summary, setSummary] = useState<string>('');
  const [isUploading, setIsUploading] = useState(false);

  const toggleDropdown = () => setIsDropdownOpen(!isDropdownOpen);

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
      setIsLoggedIn(true);
    }
  }, []);

  const handleLoginClick = () => setIsLoginModalOpen(true);
  const handleLogoutClick = () => {
    localStorage.removeItem("user");
    setUser(null);
    setIsLoggedIn(false);
  };

  const handleModalClose = () => {
    setIsLoginModalOpen(false);
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
      setIsLoggedIn(true); 
    }
  };

  const handleUploadClick = () => {
    setIsUploadModalOpen(true);
  };

  const handleUploadModalClose = () => {
    setIsUploadModalOpen(false);
  };

  // File selection handler
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0] || null;
    setFile(selectedFile);
    console.log("Selected file:", selectedFile); // Debug log
  };

  const handleUploadModalSubmit = async () => {
    if (!file) {
      alert('Please upload a recipe PDF');
      return;
    }
  
    setIsUploading(true);
    const formData = new FormData();
    formData.append('file', file);
  
    // Hardcoded test question for now, adjust as necessary
    const recipe_test_question = "Suggest a recipe for ingredients: \n\n'chicken breast, onion, white beans, chicken broth and sour cream' \n\nonly from the uploaded receipes:\n\n";
    formData.append('query', JSON.stringify({ question: recipe_test_question, user_id: user?.id || null }));
  
    console.log(`Uploading: ${file}`);

    const PROCESSING = "Processing..."
  
    try {
      // Add the new query placeholder to the chat
      const newQuery = { question: "Uploaded Recipe PDF", response: PROCESSING, timestamp: new Date() };
      setQueries(prevQueries => [...prevQueries, newQuery]);
  
      const response = await axios.post('http://localhost:8000/api/upload_pdf', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
  
      // Extract the response content similar to handleSubmit
      const responseContent = response.data?.response?.choices?.[0]?.message?.content || "No response available";
      setContext(response.data.context);
  
      // Update the response in queries to display it in the chat window
      setQueries(prevQueries => prevQueries.map(q =>
        q.question === "Uploaded Recipe PDF" && q.response === PROCESSING
          ? { ...q, response: responseContent, timestamp: new Date() }
          : q
      ));

      handleUploadModalClose(); // Close the modal on success
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('An error occurred during file upload. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

useEffect(() => {
  const initialPrompt = user
    ? `Hello ${user.username}! I'm Fridgy, your intelligent refrigerator assistant. How can I help you today?`
    : "Hello! I'm Fridgy, your intelligent refrigerator assistant. Don't forget to log in so I can help you better!";
  setQueries([
    {
      question: "Hello",
      response: initialPrompt,
      timestamp: new Date(),
    },
  ]);
}, [user]);

const handleSubmit = async (question: string) => {
  setIsLoading(true);

  try {
    const newQuery: Query = { question, response: "Thinking...", timestamp: new Date() };
    setQueries(prevQueries => [...prevQueries, newQuery]);

    const updatedContext = [...context, { role: 'user', content: question }];

    const response = await axios.post<ApiResponse>('http://localhost:8000/api/query', { 
      question,
      user_id: user?.id || null,
      context: updatedContext 
    });
    
    setContext(response.data.context);
    
    // Conditional check for response content to avoid runtime errors
    const responseContent = response.data?.response?.choices?.[0]?.message?.content || "No response available";
    
    setQueries(prevQueries => prevQueries.map(q => 
      q.question === question && q.response === "Thinking..." 
        ? { ...q, response: responseContent, timestamp: new Date() } 
        : q
    ));
  } catch (error) {
    console.error('Error during query submission:', error); // Added specific error handling
    alert('An error occurred during query submission. Please try again.');
  } finally {
    setIsLoading(false);
    setInputValue("");
  }
};


  return (
    <main className="flex min-h-screen p-6">
      <Sidebar setInputValue={setInputValue} />
      <div className="flex-grow flex flex-col justify-between ml-4">
        <div className="text-black text-center py-4 rounded-md mb-6">
          <h1 className="text-4xl">Welcome to Fridgy!</h1>
          <p className="mt-3">
            Your artificially intelligent refrigerator assistant
          </p>
          <div className="absolute top-9 right-11">
            {isLoggedIn ? (
              <div className="relative">
                <button
                  onClick={toggleDropdown}
                  onMouseEnter={() => setIsHovered(true)}
                  onMouseLeave={() => setIsHovered(false)}
                  className="flex items-center"
                >
                  <span className={clsx(
                    "mr-1",
                    isHovered ? "text-black" : "text-gray-600"
                  )}>
                    {user?.username}
                  </span>
                  <ChevronDownIcon
                    className={clsx(
                      "h-6 w-6",
                      isHovered ? "text-black" : "text-gray-600",
                    )}
                  />
                </button>
                {isDropdownOpen && (
                  <div className="absolute right-0 mt-2 w-32 bg-white border rounded shadow-lg">
                    <button
                      onClick={() => {
                        handleUploadClick();
                        toggleDropdown();
                      }}
                      className="block w-full px-4 py-2 text-left hover:bg-gray-100"
                    >
                      Upload Recipe
                    </button>
                    <button
                      onClick={() => {
                        handleLogoutClick();
                        toggleDropdown();
                      }}
                      className="block w-full px-4 py-2 text-left text-red-500 hover:bg-gray-100"
                    >
                      Logout
                    </button>
                  </div>
                )}
                {isUploadModalOpen && (
                  <UploadModal
                    onClose={handleUploadModalClose}
                    onFileChange={handleFileChange}
                    onSubmit={handleUploadModalSubmit}
                    isUploading={isUploading}
                  />
                )}
              </div>
            ) : (
              <button onClick={handleLoginClick} className="text-slate-500 hover:text-slate-600 bg-transparent">
                Login
              </button>
            )}
          </div>
        </div>
        <div className="flex-grow overflow-y-auto mb-4 p-4 rounded-lg">
          <QueryResponse queries={queries} />
        </div>
        <div className="relative w-[50%] mx-auto mb-5">
          <Search
            inputValue={inputValue}
            setInputValue={setInputValue}
            onSubmit={handleSubmit}
          />
        </div>
      </div>
      {isLoginModalOpen && <LoginModal onClose={handleModalClose} />}
    </main>
  );
};

export default ChatInterface;

const UploadModal: React.FC<{
  onClose: () => void;
  onFileChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onSubmit: () => void;
  isUploading: boolean;
}> = ({ onClose, onFileChange, onSubmit, isUploading }) => {
  // return (
  //   <div className="modal">
  //     <div className="modal-content">
  //       <h2>Upload Your Recipe</h2>
  //       <input type="file" onChange={onFileChange} accept=".pdf" />
  //       <button onClick={onSubmit} disabled={isUploading}>
  //         {isUploading ? "Uploading..." : "Upload"}
  //       </button>
  //       <button onClick={onClose}>Close</button>
  //     </div>
  //   </div>
  // );

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white p-6 rounded shadow-lg">
        <h2 className="text-lg mb-4">Upload Recipe (PDF)</h2>
        <input type="file" accept="application/pdf" onChange={onFileChange} />
        <button onClick={onSubmit} disabled={isUploading} className="mt-4 px-4 py-2 bg-blue-500 text-white rounded">
        {isUploading ? "Uploading... " : "Upload "}
        </button>
        <button onClick={onClose} className="mt-2 px-4 py-2 text-gray-500">
          Cancel
        </button>
      </div>
    </div>
  );

};
