import { API_ENDPOINTS } from "../config/api"

// Get auth token from localStorage
const getAuthToken = () => {
  return localStorage.getItem("authToken")
}

// Set auth token in localStorage
const setAuthToken = (token) => {
  localStorage.setItem("authToken", token)
}

// Remove auth token from localStorage
const removeAuthToken = () => {
  localStorage.removeItem("authToken")
}

// API request helper with authentication
const apiRequest = async (url, options = {}) => {
  const token = getAuthToken()

  const config = {
    headers: {
      "Content-Type": "application/json",
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    },
    ...options,
  }

  try {
    const response = await fetch(url, config)
    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.error || `HTTP error! status: ${response.status}`)
    }

    return data
  } catch (error) {
    console.error("API request failed:", error)
    throw error
  }
}

// Auth API calls
export const authAPI = {
  register: async (userData) => {
    const data = await apiRequest(API_ENDPOINTS.AUTH.REGISTER, {
      method: "POST",
      body: JSON.stringify(userData),
    })
    if (data.access_token) {
      setAuthToken(data.access_token)
    }
    return data
  },

  login: async (credentials) => {
    const data = await apiRequest(API_ENDPOINTS.AUTH.LOGIN, {
      method: "POST",
      body: JSON.stringify(credentials),
    })
    if (data.access_token) {
      setAuthToken(data.access_token)
    }
    return data
  },

  logout: async () => {
    try {
      await apiRequest(API_ENDPOINTS.AUTH.LOGOUT, {
        method: "POST",
      })
    } finally {
      removeAuthToken()
    }
  },

  getProfile: async () => {
    return await apiRequest(API_ENDPOINTS.AUTH.PROFILE)
  },
}

// Product API calls
export const productAPI = {
  getAll: async (filters = {}) => {
    const queryParams = new URLSearchParams()

    if (filters.category) queryParams.append("category", filters.category)
    if (filters.subCategory) queryParams.append("subCategory", filters.subCategory)
    if (filters.search) queryParams.append("search", filters.search)
    if (filters.bestseller) queryParams.append("bestseller", filters.bestseller)
    if (filters.sortBy) queryParams.append("sortBy", filters.sortBy)
    if (filters.order) queryParams.append("order", filters.order)
    if (filters.limit) queryParams.append("limit", filters.limit)

    const url = `${API_ENDPOINTS.PRODUCTS.ALL}?${queryParams.toString()}`
    return await apiRequest(url)
  },

  getById: async (id) => {
    return await apiRequest(API_ENDPOINTS.PRODUCTS.BY_ID(id))
  },

  getBestsellers: async (limit = 5) => {
    const url = `${API_ENDPOINTS.PRODUCTS.BESTSELLERS}?limit=${limit}`
    return await apiRequest(url)
  },

  getLatest: async (limit = 10) => {
    const url = `${API_ENDPOINTS.PRODUCTS.LATEST}?limit=${limit}`
    return await apiRequest(url)
  },

  getRelated: async (id, limit = 5) => {
    const url = `${API_ENDPOINTS.PRODUCTS.RELATED(id)}?limit=${limit}`
    return await apiRequest(url)
  },
}

// Cart API calls
export const cartAPI = {
  get: async () => {
    return await apiRequest(API_ENDPOINTS.CART.GET)
  },

  add: async (productId, size, quantity = 1) => {
    return await apiRequest(API_ENDPOINTS.CART.ADD, {
      method: "POST",
      body: JSON.stringify({
        product_id: productId,
        size,
        quantity,
      }),
    })
  },

  update: async (productId, size, quantity) => {
    return await apiRequest(API_ENDPOINTS.CART.UPDATE, {
      method: "PUT",
      body: JSON.stringify({
        product_id: productId,
        size,
        quantity,
      }),
    })
  },

  remove: async (productId, size) => {
    return await apiRequest(API_ENDPOINTS.CART.REMOVE, {
      method: "DELETE",
      body: JSON.stringify({
        product_id: productId,
        size,
      }),
    })
  },

  clear: async () => {
    return await apiRequest(API_ENDPOINTS.CART.CLEAR, {
      method: "DELETE",
    })
  },
}

// Order API calls
export const orderAPI = {
  get: async () => {
    return await apiRequest(API_ENDPOINTS.ORDERS.GET)
  },

  getById: async (id) => {
    return await apiRequest(API_ENDPOINTS.ORDERS.BY_ID(id))
  },

  create: async (orderData) => {
    return await apiRequest(API_ENDPOINTS.ORDERS.CREATE, {
      method: "POST",
      body: JSON.stringify(orderData),
    })
  },

  updateStatus: async (id, status) => {
    return await apiRequest(API_ENDPOINTS.ORDERS.UPDATE_STATUS(id), {
      method: "PUT",
      body: JSON.stringify({ status }),
    })
  },
}

export { getAuthToken, setAuthToken, removeAuthToken }
