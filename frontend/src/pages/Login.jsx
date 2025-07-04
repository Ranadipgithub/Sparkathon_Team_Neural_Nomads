import { useState, useContext } from "react"
import { ShopContext } from "../context/ShopContext"
import { useNavigate } from "react-router-dom"

const Login = () => {
  const [currentState, setCurrentState] = useState("Login")
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
  })
  const { login, register, loading } = useContext(ShopContext)
  const navigate = useNavigate();

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  const onSubmitHandler = async (e) => {
    e.preventDefault()

    try {
      if (currentState === "Login") {
        await login({
          email: formData.email,
          password: formData.password,
        })
        navigate("/") // Redirect to home after successful login
      } else {
        await register({
          name: formData.name,
          email: formData.email,
          password: formData.password,
        })
        navigate("/") // Redirect to home after successful registration
      }
    } catch (error) {
      // Error is already handled in context with toast
      console.error("Authentication error:", error)
    }
  }

  return (
    <div>
      <form
        onSubmit={onSubmitHandler}
        className="flex flex-col items-center w-[90%] sm:max-w-96 m-auto mt-14 gap-4 text-gray-800"
      >
        <div className="inline-flex items-center gap-2 mb-2 mt-10">
          <p className="prata-regular text-3xl">{currentState}</p>
          <hr className="border-none h-[1.5px] w-8 bg-gray-800" />
        </div>

        {currentState === "Register" && (
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleInputChange}
            className="w-full px-3 py-2 border border-gray-800"
            placeholder="Name"
            required
          />
        )}

        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleInputChange}
          className="w-full px-3 py-2 border border-gray-800"
          placeholder="Email"
          required
        />

        <input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleInputChange}
          className="w-full px-3 py-2 border border-gray-800"
          placeholder="Password"
          required
        />

        <div className="w-full flex justify-between text-sm mt-[-8px]">
          <p className="cursor-pointer">Forgot your password?</p>
          {currentState === "Login" ? (
            <p className="cursor-pointer" onClick={() => setCurrentState("Register")}>
              Create account
            </p>
          ) : (
            <p className="cursor-pointer" onClick={() => setCurrentState("Login")}>
              Login here
            </p>
          )}
        </div>

        <button
          type="submit"
          disabled={loading}
          className="bg-black text-white font-light px-8 py-2 mt-4 disabled:opacity-50"
        >
          {loading ? "Please wait..." : currentState === "Login" ? "Login" : "Sign Up"}
        </button>
      </form>
    </div>
  )
}

export default Login
