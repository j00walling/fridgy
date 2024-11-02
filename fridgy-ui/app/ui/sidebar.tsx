"use client";

import React, { useState } from "react";
import { SidebarProps } from "@/app/types/interfaces";
import { Bars4Icon } from "@heroicons/react/24/outline";
import clsx from "clsx";

const CollapsibleSidebar: React.FC<SidebarProps> = ({ setInputValue }) => {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [isHovered, setIsHovered] = useState<boolean>(false);

  const commonPrompts = [
    "What do I currently have in my fridge?",
    "Can you help me add a new item to my fridge?",
    "What ingredients do I need to make [recipe]?",
    "What recipes can I make with the ingredients I have?",
    "Can you tell me if I can make [recipe] with what I have?",
    "What food will be expiring soon?",
    "What can I make with the food that is expiring soon?",
  ];

  const toggleSidebar = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div
      className={clsx(
        "transition-all duration-300",
        isOpen ? "w-64" : "w-16",
        "p-4",
      )}
    >
      <button onClick={toggleSidebar} className="mb-4 text-xl">
        <Bars4Icon
          className={clsx(
            "h-6 w-6",
            isHovered ? "text-black" : "text-gray-400",
          )}
          onMouseEnter={() => setIsHovered(true)}
          onMouseLeave={() => setIsHovered(false)}
        />
        {isOpen && <p className="mt-5">Common Prompts</p>}
      </button>
      {isOpen && (
        <ul>
          {commonPrompts.map((prompt, index) => (
            <li
              key={index}
              className="cursor-pointer p-2 hover:bg-gray-100"
              onClick={() => setInputValue(prompt)}
            >
              {prompt}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default CollapsibleSidebar;
