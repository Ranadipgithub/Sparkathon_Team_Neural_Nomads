import { Route, Routes } from "react-router-dom"
import Home from "./pages/Home"
import Collection from "./pages/Collection"
import About from "./pages/About"
import Contact from "./pages/Contact"
import Product from "./pages/Product"
import Cart from "./pages/Cart"
import Login from "./pages/Login"
import PlaceOrder from "./pages/PlaceOrder"
import Orders from "./pages/Orders"
import Navbar from "./components/Navbar"
import Footer from "./components/Footer"
import SearchBar from "./components/SearchBar"

// Admin components
import AdminLogin from "./pages/admin/AdminLogin"
import AdminDashboard from "./pages/admin/AdminDashboard"
import AdminProducts from "./pages/admin/AdminProducts"
import AdminOrders from "./pages/admin/AdminOrders"
import AdminLayout from "./components/AdminLayout"

import VoiceAssistance from "./VoiceAssistant/VoiceAssi"
import VoiceIcon from './assets/voice.svg'

// Sonner toaster
import { Toaster } from "sonner"
import { useState } from "react"
import { useDispatch } from "react-redux"

const App = () => {
   const [popUp,setPopUp]= useState(false);
   
  const dispatch = useDispatch();
  const [camInfo,setCamInfo]=useState(false);
  const [welcome, setWelcome] = useState(false);
   
  function closePopUp() {
        setPopUp(!popUp);
    }

  // const { isLoggedIn, role } = useSelector((state) => state.auth);
  const isLoggedIn=true

  return (
    <div className="px-4 sm:px-[5vw] md:px-[7vw] lg:px-[9vw]">
      {/* Sonner toast container */}
      <Toaster position="bottom-right" richColors />

    { isLoggedIn ?

      <div>
    {popUp ? (
      <VoiceAssistance popUp={popUp} closePopUp={closePopUp}  />
    ) : null}

    {!popUp?
    <div className="fixed bottom-6 left-6 z-50">
      <div
        className="montserrat-font1 relative group h-16 w-16"
        onMouseEnter={() => setCamInfo(true)}
        onMouseLeave={() => setCamInfo(false)}
      >
        {/* Tooltip */}
        <div
          className={`
            absolute -top-[88%] left-[18vh] -translate-x-1/2 w-[15rem] px-4 py-2 rounded-lg shadow-lg 
            border border-gray-300 bg-white text-slate-700 transition-all duration-300 ease-in-out 
            z-10 ${camInfo ? 'opacity-100 scale-100' : 'opacity-0 scale-95 pointer-events-none'}
          `}
        >
        <div className=" absolute -bottom-1 left-[5vh] -translate-x-1/2 w-4 h-4 bg-white  border-gray-10 rotate-45"></div>
          Hi , I am a voice assistance !!
        </div>

        {/* Voice Button */}
        <div
          className="h-16 w-16 rounded-full bg-blue-300 shadow-lg hover:bg-blue-400 transition duration-300 flex items-center justify-center cursor-pointer"
          onClick={closePopUp}
        >
          <img src={VoiceIcon} alt="Voice" className="w-3/5 h-3/5 object-contain" />
        </div>
      </div>
    </div>:null}

      
      </div> :null    
      }
      <Routes>
        {/* Admin Routes */}
        <Route path="/admin/login" element={<AdminLogin />} />
        <Route
          path="/admin/dashboard"
          element={
            <AdminLayout>
              <AdminDashboard />
            </AdminLayout>
          }
        />
        <Route
          path="/admin/products"
          element={
            <AdminLayout>
              <AdminProducts />
            </AdminLayout>
          }
        />
        <Route
          path="/admin/orders"
          element={
            <AdminLayout>
              <AdminOrders />
            </AdminLayout>
          }
        />

        {/* Regular Routes */}
        <Route
          path="/*"
          element={
            <>
              <Navbar />
              <SearchBar />
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/collection" element={<Collection />} />
                <Route path="/about" element={<About />} />
                <Route path="/contact" element={<Contact />} />
                <Route path="/products/:productId" element={<Product />} />
                <Route path="/cart" element={<Cart />} />
                <Route path="/login" element={<Login />} />
                <Route path="/place-order" element={<PlaceOrder />} />
                <Route path="/orders" element={<Orders />} />
              </Routes>
              <Footer />
            </>
          }
        />
      </Routes>
    </div>
  )
}

export default App
