import { useState } from "react";
import axios, { AxiosResponse } from 'axios';


const CreateAccountModal = ({
  onClose,
}: {
  onClose: () => void;
}) => {
  const [newUsername, setNewUsername] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [inputError, setInputError] = useState(false);
  const [accountError, setAccountError] = useState("");


  const handleCreateAccount = async () => {
    if (newUsername && newPassword) {
      setInputError(false);
      setAccountError("");

      try {
        await axios.post("http://localhost:8000/register", {
          username: newUsername,
          password: newPassword,
        });
        onClose();
      } catch (error) {
        if (axios.isAxiosError(error)) {
          if (error.response?.status === 400) {
            setAccountError("An account with this username already exists.");
          } 
        } else {
            setAccountError("An unexpected error occured.");
        }
      }
    } else {
      setInputError(true);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h2 className="text-2xl mb-4">Create Account</h2>
        {inputError && <p className="text-red-500 mb-2">Please fill in all fields.</p>}
        {accountError && <p className="text-red-500 mb-2">{accountError}</p>}
        <input
          type="text"
          placeholder="Username"
          value={newUsername}
          onChange={(e) => setNewUsername(e.target.value)}
          className={`rounded-md border ${inputError && !newUsername ? "border-red-500" : "border-gray-200"} p-2 w-full mb-4 placeholder:text-gray-500 focus:border-gray-400 focus:ring-0 outline-2 text-sm`}
        />
        <input
          type="password"
          placeholder="Password"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
          className={`rounded-md border ${inputError && !newUsername ? "border-red-500" : "border-gray-200"} p-2 w-full mb-4 placeholder:text-gray-500 focus:border-gray-400 focus:ring-0 outline-2 text-sm`}
        />
        <button onClick={handleCreateAccount} className="bg-blue-500 text-white px-4 py-2 rounded mr-3">
          Create Account
        </button>
        <button onClick={onClose} className="ml-2 text-gray-500">
          Cancel
        </button>
      </div>
    </div>
  );
};

const LoginModal = ({ onClose }: { onClose: () => void }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isCreatingAccount, setIsCreatingAccount] = useState(false);
  const [loginError, setLoginError] = useState("");
  const [inputError, setInputError] = useState(false);

  const handleLogin = async () => {
    try {
      const response = await axios.post("http://localhost:8000/login", { username, password });
  
      setLoginError("");
      setInputError(false);
  
      if (response.status === 200) {
        const { id, username } = response.data;
        localStorage.setItem("user", JSON.stringify({ id, username }));
        onClose();
      }
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.status === 401) {
        setLoginError("Invalid username or password.");
      } else {
        setLoginError("Login failed: An unexpected error occurred.");
      }
    }
  };

  return (
    <div>
      <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
        <div className="bg-white p-6 rounded-lg shadow-lg">
          <h2 className="text-2xl mb-4">Login</h2>
          {loginError && <p className="text-red-500 mb-2">{loginError}</p>}
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className={`rounded-md border ${inputError ? "border-red-500" : "border-gray-200"} p-2 w-full mb-4 placeholder:text-gray-500 focus:border-gray-400 focus:ring-0 outline-2 text-sm`}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className={`rounded-md border ${inputError ? "border-red-500" : "border-gray-200"} p-2 w-full mb-4 placeholder:text-gray-500 focus:border-gray-400 focus:ring-0 outline-2 text-sm`}
          />
          <button onClick={handleLogin} className="bg-blue-500 text-white px-4 py-2 rounded mr-3">
            Login
          </button>
          <button onClick={onClose} className="ml-2 text-gray-500">
            Cancel
          </button>
          <p
            className="text-blue-500 cursor-pointer mt-4 text-sm"
            onClick={() => setIsCreatingAccount(true)}
          >
            Create an account
          </p>
        </div>
      </div>

      {isCreatingAccount && <CreateAccountModal onClose={() => setIsCreatingAccount(false)} />}
    </div>
  );
};

export default LoginModal;
