"use client";

import { useState, useEffect } from "react";
import axios from "axios";
import Search from "@/app/ui/search";
import LoginModal from "@/app/ui/login";
import QueryResponse from "@/app/ui/query-response";
import Sidebar from "@/app/ui/sidebar";
import { Query } from "@/app/types/interfaces";
import { ChevronDownIcon } from "@heroicons/react/24/outline";
import clsx from "clsx";

const PROCESSING = "Processing...";
const DEFAULT_RECIPE_TEST_QUESTION = "Suggest a recipe based on what's in my fridge's inventory, only from the uploaded recipes:\n\n";
const DEFAULT_IMAGE_TEST_QUESTION = "Add the following food items seen in the uploaded picture to my fridge's inventory:\n\n";
const UPLOAD_MODAL_TYPE = {
  PDF: "PDF",
  IMAGE: "IMAGE",
};

interface ApiResponse {
  response: {
    id: string;
    choices: Array<{
      message: { content: string };
    }>;
    context: Array<{ role: string; content: string }>;
  };
}

interface User {
  id: number;
  username: string;
}

const ChatInterface = () => {
  const [inputValue, setInputValue] = useState("");
  const [queries, setQueries] = useState<Query[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [context, setContext] = useState([]);
  const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState<User | null>(null);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [isHovered, setIsHovered] = useState(false);
  
  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
  const [uploadModalType, setUploadModalType] = useState<"PDF" | "IMAGE" | null>(null);
  
  const [file, setFile] = useState<File | null>(null);
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

  const handleUploadClick = (type: "PDF" | "IMAGE") => {
    setUploadModalType(type);
    setIsUploadModalOpen(true);
  };

  const handleUploadModalClose = () => {
    setIsUploadModalOpen(false);
    setUploadModalType(null);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0] || null;
    setFile(selectedFile);
  };

  const handleUploadSubmit = async () => {
    if (!file) {
      alert(`Please upload a ${uploadModalType === "PDF" ? "recipe PDF" : "inventory image"}`);
      return;
    }

    setIsUploading(true);
    const formData = new FormData();
    formData.append("file", file);
    formData.append("query", JSON.stringify({
      question: uploadModalType === "PDF" ? DEFAULT_RECIPE_TEST_QUESTION : DEFAULT_IMAGE_TEST_QUESTION,
      user_id: user?.id || null,
    }));

    const queryTitle = uploadModalType === "PDF" ? "Uploaded Recipe PDF" : "Uploaded Grocery Picture";
    const newQuery: Query = { question: queryTitle, response: PROCESSING, timestamp: new Date() };
    setQueries(prevQueries => [...prevQueries, newQuery]);

    try {
      const apiEndpoint = uploadModalType === "PDF" ? "upload_pdf" : "upload_image";
      const response = await axios.post(`http://localhost:8000/api/${apiEndpoint}`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      const responseContent = response.data?.response?.choices?.[0]?.message?.content || "No response available";
      setContext(response.data.context);

      setQueries(prevQueries => prevQueries.map(q =>
        q.question === queryTitle && q.response === PROCESSING
          ? { ...q, response: responseContent, timestamp: new Date() }
          : q
      ));

      handleUploadModalClose();
    } catch (error) {
      console.error(`Error uploading ${uploadModalType}:`, error);
      alert(`An error occurred during ${uploadModalType} upload. Please try again.`);
    } finally {
      setIsUploading(false);
    }
  };

  useEffect(() => {
    const initialPrompt = user
      ? `Hello ${user.username}! I'm Fridgy, your intelligent refrigerator assistant. How can I help you today?`
      : "Hello! I'm Fridgy, your intelligent refrigerator assistant. Don't forget to log in so I can help you better!";
    setQueries([{ question: "Hello", response: initialPrompt, timestamp: new Date() }]);
  }, [user]);

  const handleSubmit = async (question: string) => {
    setIsLoading(true);

    try {
      const newQuery: Query = { question, response: "Thinking...", timestamp: new Date() };
      setQueries(prevQueries => [...prevQueries, newQuery]);

      const updatedContext = [...context, { role: "user", content: question }];

      const response = await axios.post<ApiResponse>("http://localhost:8000/api/query", {
        question,
        user_id: user?.id || null,
        context: updatedContext,
      });

      setContext(response.data.context);
      const responseContent = response.data?.response?.choices?.[0]?.message?.content || "No response available";

      setQueries(prevQueries => prevQueries.map(q =>
        q.question === question && q.response === "Thinking..."
          ? { ...q, response: responseContent, timestamp: new Date() }
          : q
      ));
    } catch (error) {
      console.error("Error during query submission:", error);
      alert("An error occurred during query submission. Please try again.");
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
          <p className="mt-3">Your artificially intelligent refrigerator assistant</p>
          <div className="absolute top-9 right-11">
            {isLoggedIn ? (
              <div className="relative">
                <button onClick={toggleDropdown} onMouseEnter={() => setIsHovered(true)} onMouseLeave={() => setIsHovered(false)} className="flex items-center">
                  <span className={clsx("mr-1", isHovered ? "text-black" : "text-gray-600")}>{user?.username}</span>
                  <ChevronDownIcon className={clsx("h-6 w-6", isHovered ? "text-black" : "text-gray-600")} />
                </button>
                {isDropdownOpen && (
                  <div className="absolute right-0 mt-2 w-32 bg-white border rounded shadow-lg">
                    <button onClick={() => { handleUploadClick("PDF"); toggleDropdown(); }} className="block w-full px-4 py-2 text-left hover:bg-gray-100">Upload Recipe</button>
                    <button onClick={() => { handleUploadClick("IMAGE"); toggleDropdown(); }} className="block w-full px-4 py-2 text-left hover:bg-gray-100">Upload Grocery Picture</button>
                    <button onClick={() => { handleLogoutClick(); toggleDropdown(); }} className="block w-full px-4 py-2 text-left text-red-500 hover:bg-gray-100">Logout</button>
                  </div>
                )}
                {isUploadModalOpen && (
                  <UploadModal
                    onClose={handleUploadModalClose}
                    onFileChange={handleFileChange}
                    onSubmit={handleUploadSubmit}
                    isUploading={isUploading}
                    type={uploadModalType}
                  />
                )}
              </div>
            ) : (
              <button onClick={handleLoginClick} className="text-slate-500 hover:text-slate-600 bg-transparent">Login</button>
            )}
          </div>
        </div>
        <div className="flex-grow overflow-y-auto mb-4 p-4 rounded-lg">
          <QueryResponse queries={queries} />
        </div>
        <div className="relative w-[50%] mx-auto mb-5">
          <Search inputValue={inputValue} setInputValue={setInputValue} onSubmit={handleSubmit} />
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
  type: "PDF" | "IMAGE" | null;
}> = ({ onClose, onFileChange, onSubmit, isUploading, type }) => (
  <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
    <div className="bg-white p-6 rounded shadow-lg">
      <h2 className="text-lg mb-4">{type === "PDF" ? "Upload Recipe (PDF)" : "Upload Inventory Image (JPG)"}</h2>
      <input type="file" accept={type === "PDF" ? "application/pdf" : "image/*"} onChange={onFileChange} />
      <button onClick={onSubmit} disabled={isUploading} className="mt-4 px-4 py-2 bg-blue-500 text-white rounded">
        {isUploading ? "Uploading..." : "Upload"}
      </button>
      <button onClick={onClose} className="mt-2 px-4 py-2 text-gray-500">Cancel</button>
    </div>
  </div>
);