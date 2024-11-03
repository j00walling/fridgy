export interface Query {
  question: string;
  response: string;
  timestamp: Date; 
}

export interface ApiResponse {
  answer: string;
}

export interface SearchProps {
  inputValue: string;
  setInputValue: (value: string) => void;
  setQueries: (updater: (prevQueries: Query[]) => Query[]) => void;
}

export interface SidebarProps {
  setInputValue: (value: string) => void;
}
