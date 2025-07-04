// API configuration for Vite
const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:5328/api"

export const API_ENDPOINTS = {
  // Auth endpoints
  AUTH: {
    REGISTER: `${API_BASE_URL}/auth/register`,
    LOGIN: `${API_BASE_URL}/auth/login`,
    PROFILE: `${API_BASE_URL}/auth/profile`,
    LOGOUT: `${API_BASE_URL}/auth/logout`,
  },

  // Product endpoints
  PRODUCTS: {
    ALL: `${API_BASE_URL}/products`,
    BY_ID: (id) => `${API_BASE_URL}/products/${id}`,
    BESTSELLERS: `${API_BASE_URL}/products/bestsellers`,
    LATEST: `${API_BASE_URL}/products/latest`,
    RELATED: (id) => `${API_BASE_URL}/products/related/${id}`,
  },

  // Cart endpoints
  CART: {
    GET: `${API_BASE_URL}/cart`,
    ADD: `${API_BASE_URL}/cart/add`,
    UPDATE: `${API_BASE_URL}/cart/update`,
    REMOVE: `${API_BASE_URL}/cart/remove`,
    CLEAR: `${API_BASE_URL}/cart/clear`,
  },

  // Order endpoints
  ORDERS: {
    GET: `${API_BASE_URL}/orders`,
    BY_ID: (id) => `${API_BASE_URL}/orders/${id}`,
    CREATE: `${API_BASE_URL}/orders/create`,
    UPDATE_STATUS: (id) => `${API_BASE_URL}/orders/${id}/status`,
  },
}

export default API_BASE_URL
