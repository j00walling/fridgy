"use client";

import { useState, useEffect } from "react";
import axios, { AxiosResponse } from 'axios';
import Search from "@/app/ui/search";
import QueryResponse from "@/app/ui/query-response";
import Sidebar from "@/app/ui/sidebar";
import { Query } from "@/app/types/interfaces";

interface ApiResponse {
  response: string;
  context: Array<{role: string, content: string}>;
}

function isAxiosResponse(response: any): response is AxiosResponse<ApiResponse> {
  return response && typeof response === 'object' && 'data' in response;
}

const ChatInterface = () => {
  const [inputValue, setInputValue] = useState<string>("");
  const [queries, setQueries] = useState<Query[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [context, setContext] = useState<Array<{role: string, content: string}>>([]);

useEffect(() => {
  console.log("Context updated:", context);
}, [context]);

  useEffect(() => {
    setQueries([{ 
      question: "Hello", 
      response: "Hello! I'm Fridgy, your intelligent refrigerator assistant. How can I help you today?",
      timestamp: new Date()  // Add this line
    }]);
  }, []);

  const handleSubmit = async (question: string) => {
    console.log("Submitting question:", question);
    setIsLoading(true);
    
    try {
      const newQuery: Query = { question, response: "Thinking...", timestamp: new Date() };
      setQueries(prevQueries => [...prevQueries, newQuery]);
  
      // Update context with the new user message
      const updatedContext = [...context, { role: 'user', content: question }];
  
      const response = await axios.post<ApiResponse>('http://localhost:8000/api/query', { 
        question, 
        context: updatedContext 
      });
      
      console.log("Received response:", response.data.response);
      console.log("Updated context:", response.data.context);
      
      // Update the context with the new response
      setContext(response.data.context);
      
      setQueries(prevQueries => prevQueries.map(q => 
        q.question === question && q.response === "Thinking..." 
          ? { ...q, response: response.data.response, timestamp: new Date() } 
          : q
      ));
    } catch (error) {
      // ... error handling ...
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
        </div>
        <div className="flex-grow overflow-y-auto">
          <QueryResponse queries={queries} />
        </div>
        <div className="relative w-[50%] mx-auto mb-5">
          <Search
            inputValue={inputValue}
            setInputValue={setInputValue}
            onSubmit={handleSubmit}
            isLoading={isLoading}
          />
        </div>
      </div>
    </main>
  );
};

export default ChatInterface;