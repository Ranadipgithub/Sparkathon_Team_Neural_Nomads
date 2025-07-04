import React, { use, useContext, useEffect, useState } from 'react'
import { ShopContext } from '../context/ShopContext'
import { assets } from '../assets/assets';
import Title from '../components/Title'
import ProductItem from '../components/ProductItem';

const Collection = () => {
  const {products, search, showSearch} = useContext(ShopContext);
  const [showFilters, setShowFilters] = useState(false);
  const [filterProducts, setFilterProducts] = useState([]);
  const [category, setCategory] = useState([]);
  const [subCategory, setSubCategory] = useState([]);
  const [sortType, setSortType] = useState('relevent');

  const toggleCategory = (e) => {
    if(category.includes(e.target.value)){
      setCategory(category.filter((item) => item !== e.target.value));
    }else{
      setCategory([...category, e.target.value]);
    }
  }

  const toggleSubCategory = (e) => {
    if(subCategory.includes(e.target.value)){
      setSubCategory(subCategory.filter((item) => item !== e.target.value));
    }else{
      setSubCategory([...subCategory, e.target.value]);
    }
  }

  const applyFilter = () => {
    let filteredProducts = products.slice();
    if(showSearch && search.length > 0){
      filteredProducts = filteredProducts.filter((product) => product.name.toLowerCase().includes(search.toLowerCase()));
    }
    if(category.length > 0){
      filteredProducts = filteredProducts.filter((product) => category.includes(product.category));
    }
    if(subCategory.length > 0){
      filteredProducts = filteredProducts.filter((product) => subCategory.includes(product.subCategory));
    }
    setFilterProducts(filteredProducts);
  }

  const sortProduct = () => {
    let fpCopy = filterProducts.slice();
    switch (sortType) {
      case 'low-high':
        setFilterProducts(fpCopy.sort((a, b) => a.price - b.price));
        break;
      case 'high-low':
        setFilterProducts(fpCopy.sort((a, b) => b.price - a.price));
        break;
      default:
        applyFilter();
        break;
    }
  }

  useEffect(()=>{
    applyFilter();
  }, [category, subCategory, search, showSearch])

  useEffect(()=>{
    sortProduct();
  }, [sortType])

  return (
    <div className='flex flex-col sm:flex-row gap-1 sm:gap-10 pt-10 border-t'>
      <div className='min-w-60'>
        <p onClick={() => setShowFilters(!showFilters)} className='my-2 text-xl flex items-center cursor-pointer gap-2'>FILTERS <img src={assets.dropdown_icon} alt="" className={`h-3 sm:hidden ${showFilters ? 'rotate-90' : ''}`} /> </p>
        <div className={`border border-gray-300 pl-5 py-3 mt-6 ${showFilters ? '' : 'hidden'} sm:block`}>
          <p className='mb-3 text-sm font-medium'>CATEGORIES</p>
          <div className='flex flex-col gap-2 text-sm font-light text-gray-700'>
            <p className='flex gap-2'>
              <input onChange={toggleCategory} type="checkbox" className='w-3' value={'Men'}/>Men
            </p>
            <p className='flex gap-2'>
              <input onChange={toggleCategory} type="checkbox" className='w-3' value={'Women'}/>Women
            </p>
            <p className='flex gap-2'>
              <input onChange={toggleCategory} type="checkbox" className='w-3' value={'Kids'}/>Kids
            </p>
          </div>
        </div>

        <div className={`border border-gray-300 pl-5 py-3 my-5 ${showFilters ? '' : 'hidden'} sm:block`}>
          <p className='mb-3 text-sm font-medium'>TYPE</p>
          <div className='flex flex-col gap-2 text-sm font-light text-gray-700'>
            <p className='flex gap-2'>
              <input onChange={toggleSubCategory} type="checkbox" className='w-3' value={'Topwear'}/>Topwear
            </p>
            <p className='flex gap-2'>
              <input onChange={toggleSubCategory} type="checkbox" className='w-3' value={'Bottomwear'}/>Bottomwear
            </p>
            <p className='flex gap-2'>
              <input onChange={toggleSubCategory} type="checkbox" className='w-3' value={'Winterwear'}/>Winterwear
            </p>
          </div>
        </div>
      </div>

      <div className='flex-1'>
        <div className='flex justify-between text-base sm:text-2xl mb-4'>
          <Title text1={'OUR'} text2={'COLLECTIONS'} />
          {/* product sort */}
          <select onChange={(e) => setSortType(e.target.value)} className='border-2 border-gray-300 text-sm px-2'>
            <option value="relevent">Sort by: Relevent</option>
            <option value="low-high">Sort by: Low to High</option>
            <option value="high-low">Sort by: High to Low</option>
          </select>
        </div>

        {/* map product */}
        <div className='grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 gap-y-6'>
          {
            filterProducts.map((item, index) => (
              <ProductItem key={index} id={item._id} image={item.image} name={item.name} price={item.price} />
            ))
          }
        </div>

      </div>

    </div>
  )
}

export default Collection
