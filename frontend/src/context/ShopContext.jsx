"use client"

import { createContext, useState, useEffect } from "react"
import { toast } from "sonner"
import { useNavigate } from "react-router-dom"
import { productAPI, cartAPI, authAPI, getAuthToken } from "../utils/api"

export const ShopContext = createContext()

const ShopContextProvider = ({ children }) => {
  const currency = "$"
  const delivery_fee = 10
  const [search, setSearch] = useState("")
  const [showSearch, setShowSearch] = useState(false)
  const [cartItems, setCartItems] = useState([])
  const [products, setProducts] = useState([])
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  // Check if user is authenticated
  const isAuthenticated = () => {
    return !!getAuthToken()
  }

  // Load products on component mount
  useEffect(() => {
    loadProducts()
  }, [])

  // Load user profile if authenticated
  useEffect(() => {
    if (isAuthenticated()) {
      loadUserProfile()
      loadCart()
    }
  }, [])

  const loadProducts = async () => {
    try {
      setLoading(true)
      const response = await productAPI.getAll()
      setProducts(response.products || [])
    } catch (error) {
      console.error("Error loading products:", error)
      toast.error("Failed to load products")
    } finally {
      setLoading(false)
    }
  }

  const loadUserProfile = async () => {
    try {
      const response = await authAPI.getProfile()
      setUser(response.user)
    } catch (error) {
      console.error("Error loading user profile:", error)
      if (error.message.includes("401")) {
        logout()
      }
    }
  }

  const loadCart = async () => {
    try {
      console.log("Loading cart...")
      const response = await cartAPI.get()
      console.log("Cart API response:", response)

      if (response.success && response.cart_items) {
        setCartItems(response.cart_items)
        console.log("Cart items set:", response.cart_items)
      } else {
        setCartItems([])
        console.log("No cart items found")
      }
    } catch (error) {
      console.error("Error loading cart:", error)
      setCartItems([])
    }
  }

  const addToCart = async (itemId, size) => {
    if (!size) {
      toast.error("Please select a size")
      return
    }

    if (!isAuthenticated()) {
      toast.error("Please login to add items to cart")
      navigate("/login")
      return
    }

    try {
      console.log("Adding to cart:", { itemId, size })
      const response = await cartAPI.add(itemId, size, 1)
      console.log("Add to cart response:", response)

      if (response.success) {
        await loadCart() // Reload cart after adding
        toast.success("Item added to cart")
      } else {
        toast.error("Failed to add item to cart")
      }
    } catch (error) {
      console.error("Error adding to cart:", error)
      toast.error("Failed to add item to cart")
    }
  }

  const getCartCount = () => {
    if (!Array.isArray(cartItems)) {
      return 0
    }
    return cartItems.reduce((total, item) => total + item.quantity, 0)
  }

  const updateQuantity = async (itemId, size, quantity) => {
    if (!isAuthenticated()) {
      toast.error("Please login to update cart")
      return
    }

    try {
      if (quantity <= 0) {
        await cartAPI.remove(itemId, size)
      } else {
        await cartAPI.update(itemId, size, quantity)
      }
      await loadCart() // Reload cart after updating
    } catch (error) {
      console.error("Error updating cart:", error)
      toast.error("Failed to update cart")
    }
  }

  const getCartAmount = () => {
    if (!Array.isArray(cartItems)) {
      return 0
    }
    return cartItems.reduce((total, item) => {
      if (item.product) {
        return total + item.product.price * item.quantity
      }
      return total
    }, 0)
  }

  const login = async (credentials) => {
    try {
      setLoading(true)
      const response = await authAPI.login(credentials)
      setUser(response.user)
      await loadCart()
      toast.success("Login successful")
      return response
    } catch (error) {
      console.error("Login error:", error)
      toast.error(error.message || "Login failed")
      throw error
    } finally {
      setLoading(false)
    }
  }

  const register = async (userData) => {
    try {
      setLoading(true)
      const response = await authAPI.register(userData)
      setUser(response.user)
      toast.success("Registration successful")
      return response
    } catch (error) {
      console.error("Registration error:", error)
      toast.error(error.message || "Registration failed")
      throw error
    } finally {
      setLoading(false)
    }
  }

  const logout = async () => {
    try {
      await authAPI.logout()
    } catch (error) {
      console.error("Logout error:", error)
    } finally {
      setUser(null)
      setCartItems([])
      toast.success("Logged out successfully")
      navigate("/")
    }
  }

  const clearCart = async () => {
    if (!isAuthenticated()) return

    try {
      await cartAPI.clear()
      setCartItems([])
    } catch (error) {
      console.error("Error clearing cart:", error)
    }
  }

  const value = {
    products,
    currency,
    delivery_fee,
    search,
    setSearch,
    showSearch,
    setShowSearch,
    cartItems,
    addToCart,
    getCartCount,
    updateQuantity,
    getCartAmount,
    navigate,
    user,
    login,
    register,
    logout,
    isAuthenticated,
    loading,
    loadProducts,
    clearCart,
    loadCart,
  }

  return <ShopContext.Provider value={value}>{children}</ShopContext.Provider>
}

export default ShopContextProvider
