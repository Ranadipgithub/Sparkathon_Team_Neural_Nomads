import { createContext, useState } from "react";
import { products } from "../assets/assets";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";

export const ShopContext = createContext();

const ShopContextProvider = ({ children }) => {
    const currency = "$";
    const delivery_fee = 10;
    const [search, setSearch] = useState('');
    const [showSearch, setShowSearch] = useState(false);
    const [cartItems, setCartItems] = useState({});
    const navigate = useNavigate();

    const addToCart = (itemId, size) => {
        if(!size) toast.error('Please select a size');
        let cartData = structuredClone(cartItems);
        if (cartData[itemId]) {
            if(cartData[itemId][size]) {
                cartData[itemId][size] += 1;
            } else{
                cartData[itemId][size] = 1;
            }
        } else {
            cartData[itemId] = {};
            cartData[itemId][size] = 1;
        }
        setCartItems(cartData);
    };

    const getCartCount = () => {
        let count = 0;
        for (const key in cartItems) {
            for (const size in cartItems[key]) {
                try{
                    if(cartItems[key][size] > 0){
                        count += cartItems[key][size];
                    }
                }catch(err){
                }
            }
        }
        return count;
    };

    const updateQuantity = (itemId, size, quantity) => {
        let cartData = structuredClone(cartItems);
        cartData[itemId][size] = quantity;
        setCartItems(cartData);
    };

    const getCartAmount = () => {
        let totalAmount = 0;
        for(const items in cartItems){
            let itemInfo = products.find((product) => product._id === items);
            for(const item in cartItems[items]){
                try{
                    if(cartItems[items][item] > 0){
                    totalAmount += itemInfo.price * cartItems[items][item];
                }
                }catch(err){
                }
            }
        }
        return totalAmount;
    };
    
    const value = {
        products,
        currency,
        delivery_fee,
        search, setSearch,
        showSearch, setShowSearch,
        cartItems, addToCart,
        getCartCount, updateQuantity,
        getCartAmount, navigate
    }
    return <ShopContext.Provider value={value}>{children}</ShopContext.Provider>;
};

export default ShopContextProvider;